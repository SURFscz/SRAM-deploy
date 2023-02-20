#!/usr/bin/env python3
import subprocess
import json

result = subprocess.run("/bin/journalctl -u plsc -n 3 JOB_TYPE=start -o json",
                        shell=True, encoding='UTF-8', capture_output=True)
output = result.stdout.strip()

start = 0
end = 0
started = False
for line in output.split("\n"):
  try:
    log = json.loads(line)
  except Exception:
    break
  message = log['MESSAGE']
  timestamp = int(log['__MONOTONIC_TIMESTAMP'])
  if 'Starting' in message:
      start = timestamp
      started = True
  if started and 'Finished' in message:
      end = timestamp

duration = round((end - start) / 1000000)
print(duration)
