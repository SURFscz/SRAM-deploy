#!/usr/bin/env python3
import sys
import ldif
from collections import OrderedDict


def kcmp(item):
    (key, v) = item
    parts = key.split(',')[::-1]
    new_key = ','.join(parts)
    return (new_key, v)


def freeze(o):
    if isinstance(o, dict):
        return OrderedDict({k: freeze(v) for k, v in sorted(o.items(), key=kcmp)}.items())
    if isinstance(o, list):
        return sorted([freeze(v) for v in o])
    return o.decode('utf-8')


def my_print(o, depth):
    if isinstance(o, OrderedDict):
        for k, v in o.items():
            if k in ("contextCSN", "entryCSN", "modifyTimestamp", "modifiersName"):
                continue
            my_print(k, depth)
            my_print(v, depth + 2)
    elif isinstance(o, list):
        for v in o:
            my_print(v, depth)
    else:
        print(f"{' ' * depth}{o}")


ldifparser = ldif.LDIFRecordList(sys.stdin)
ldifparser.parse()

data = {k: v for k, v in ldifparser.all_records}
f = freeze(data)

# print(json.dumps(f, indent=2))
my_print(f, 0)
