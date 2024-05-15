#!/usr/bin/env python3
import sys
import subprocess
import json

#
# This script outputs how long the latest complete plsc run took
# We do this by going through the revelant syslog messages in reverse order
# and recording the tiemstamps of the latest full cycle (start/finished)
#

result = subprocess.run("/bin/journalctl -u plsc -n100 -r JOB_TYPE=start -o json",
                        shell=True, encoding='UTF-8', capture_output=True)
output = result.stdout.strip()

start = 0
end = 0
counting = False
for line in output.split("\n"):
    try:
        log = json.loads(line)
    except Exception:
        print(f"Failed to load json message: {log}")
        sys.exit(-1)

    message = log['MESSAGE']
    timestamp = int(log['__MONOTONIC_TIMESTAMP'])

    if not counting and 'Finished' in message:
        #print(f"found  stop={timestamp}")
        #print(f"       diff={timestamp-start}")
        end = timestamp
        counting = True
    if counting and 'Starting' in message:
        #print(f"found start={timestamp}")
        start = timestamp
        break

duration = 1e-6 * (end - start)
print(f"{duration:.3}")
