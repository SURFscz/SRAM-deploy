#!/usr/bin/env python3
from __future__ import print_function
import sys
from pprint import pprint
import yaml
from typing import Dict, Tuple, Set


def cmp_two_dicts(data1: Dict, data2: Dict) -> Tuple[Set, Set, Set]:
    # from https://stackoverflow.com/questions/3697432/how-to-find-list-intersection/33067553
    keys_data1 = set(data1.keys())
    keys_data2 = set(data2.keys())

    keys_both  = set([x for x in keys_data1 if x     in keys_data2])
    keys_only1 = set([x for x in keys_data1 if x not in keys_data2])
    keys_only2 = set([x for x in keys_data2 if x not in keys_data1])

    return (keys_both, keys_only1, keys_only2)


def cmp_two_files(file1: str, file2: str) -> None:

    print("Checking {}<->{}... ".format(file1, file2), end='')

    try:
        with open(file1, encoding='utf-8') as f:
            data1 = yaml.safe_load(f.read())
        with open(file2, encoding='utf-8') as f:
            data2 = yaml.safe_load(f.read())
    except Exception as e:
        print("failed: {}".format(e))
        sys.exit(1)
    else:
        print("found")

    (both, only1, only2) = cmp_two_dicts(data1, data2)
    for x in data1:
        if x in only1:
            print(f"Key {x} is only in {file1}")
        elif x in only2:
            print(f"Key {x} is only in {file2}")
        else:
            print(f"Key {x} is ok")

    return


cmp_two_files("environments/surf/group_vars/test.yml", "environments/surf/group_vars/pilot.yml")


sys.exit(0)
