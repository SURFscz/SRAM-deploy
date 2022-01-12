#!/usr/bin/env python3

import sys
import yaml
from typing import Dict, Any

# this generates a docker-compose.yml file for SCZ
CI_OPTION = "--ci"

ci_enabled = False
if len(sys.argv) > 1 and sys.argv[1] == CI_OPTION:
  ci_enabled = True

# these are the Docker containers that need to be spun up
hosts = {
    'sbs':      27,
    'db':       28,
}
if ci_enabled:
    hosts.update({
        'test':     30,
    })
else:
    hosts.update({
        'ldap1':    20,
        'ldap2':    21,
        'meta':     23,
        'lb':       24,
        'client':   25,
        'sandbox1': 26,
        'bhr':      29,
    })

# these are the hostnames of virtual hosts on the loadbalancer
logical_hosts = [
    'mdq',         'cm',        'comanage', 'ldap',
    'meta',        'oidc-test', 'sp-test',  'idp-test',
    'google-test', 'sbs',       'sandbox1', 'pam',
    'oidc-op',
]

extra_options = {}
if ci_enabled:
    extra_options = {
        'sbs': {
            'depends_on': [ 'db', 'redis', 'test' ],
            'volumes': ['../ci-runner:/tmp/ci-runner'],
        },
    }

subnet = '172.20.1'
domain = 'scz-vm.net'


# generates config for a single host
def host_config(num: int, name: str) -> Dict[str, Any]:
    data: Dict[str, Any] = dict()
    data['image'       ] = 'scz-base'
    data['hostname'    ] =  name
    data['volumes'     ] = [ './ansible_key.pub:/tmp/authorized_keys', '/sys/fs/cgroup:/sys/fs/cgroup:ro' ]
    data['tmpfs'       ] = [ '/run', '/run/lock', '/tmp' ]
    data['privileged'  ] = False
    data['security_opt'] = [ 'seccomp:unconfined', 'apparmor:unconfined' ]
    data['cap_add'     ] = [ 'SYS_ADMIN', 'SYS_PTRACE' ]
    data['networks'    ] = {
        'scznet': {
            'ipv4_address': f'{subnet}.{num}',
            'aliases':      [ f'{name}.vm.{domain}' ]
        }
    }
    if not ci_enabled:
        data['extra_hosts'] = [ f'{h}.{domain}:{subnet}.{hosts["lb"]}' for h in logical_hosts ]
    data['healthcheck'] = {
        'test': [ 'CMD', '/usr/bin/test', '!', '-e', '/etc/nologin' ],
        'interval': '5s',
        'timeout': '1s',
        'retries': 1,
        'start_period': '0s'
    }

    if extra_options.get(name):
        for key, value in extra_options[name].items():
            if data.get(key):
                data[key] += value
            else:
                data[key] = value

    return data

def mail_config(num: int, name: str) -> Dict[str,Any]:
    data: Dict[str, Any] = dict()
    data['image'       ] = 'mailhog/mailhog:v1.0.1'
    data['hostname'    ] =  name
    data['ports'       ] = [ 8025 ]
    data['networks'    ] = {
        'scznet': {
            'ipv4_address': f'{subnet}.{num}',
            'aliases':      [ f'{name}.vm.{domain}' ]
        }
    }
    if not ci_enabled:
        data['extra_hosts'] = [ f'{h}.{domain}:{subnet}.{hosts["lb"]}' for h in logical_hosts ]
    data['healthcheck'] = {
        'test': [ 'CMD', '/usr/bin/test', '!', '-e', '/etc/nologin' ],
        'interval': '5s',
        'timeout': '1s',
        'retries': 1,
        'start_period': '0s'
    }

    return data

def redis_config(num: int, name: str) -> Dict[str,Any]:
    data: Dict[str, Any] = dict()
    data['image'       ] = 'redis:6'
    data['hostname'    ] =  name
    data['ports'       ] = [ 6379 ]
    data['networks'    ] = {
        'scznet': {
            'ipv4_address': f'{subnet}.{num}',
            'aliases':      [ f'{name}.vm.{domain}' ]
        }
    }
    if not ci_enabled:
        data['extra_hosts'] = [ f'{h}.{domain}:{subnet}.{hosts["lb"]}' for h in logical_hosts ]
    data['healthcheck'] = {
        'test': [ 'CMD', '/usr/bin/test', '!', '-e', '/etc/nologin' ],
        'interval': '5s',
        'timeout': '1s',
        'retries': 1,
        'start_period': '0s'
    }

    return data

# generate the full docker-compose.yml file
compose: Dict[str, Any] = dict()
compose['version' ] = '2.4'
compose['networks'] = {
    'scznet': {
        'driver': 'bridge',
        'ipam': {
            'driver': 'default',
            'config': [ { 'subnet': f'{subnet}.0/24', 'gateway': f'{subnet}.1' } ]
        },
        'driver_opts': { "com.docker.network.bridge.name": "br-sram" }
    }
}
compose['services'] = { h: host_config(ip, h) for h, ip in hosts.items() }

# Add redis host on .98
compose['services']['redis'] = redis_config(98, 'redis')

# Add mail test host on .99
if not ci_enabled:
    compose['services']['mail'] = mail_config(99, 'mail')

# dump the yaml
print("---")
print("# This file has been automatically generated.  DO NOT EDIT, CHANGES WILL BE LOST!")
print("# yamllint disable")
print(yaml.dump(compose))
