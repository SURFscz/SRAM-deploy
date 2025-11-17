#!/usr/bin/env python3
"""
Generate a docker-compose.yml file for SRAM
"""

import yaml
from typing import Dict, Any
import argparse

# parse command line arguments --ci and --container using argparse
# --ci: this generates a docker-compose.yml file for CI
# --container: this generates a docker-compose.yml file for SCZ
parser = argparse.ArgumentParser(description='Generate a docker-compose.yml file for SCZ or CI')
group = parser.add_mutually_exclusive_group()
group.add_argument('--ci', action='store_true', help='generate a docker-compose.yml file for CI')
group.add_argument('--container', action='store_true', help='generate a docker-compose.yml file for SCZ')
args = parser.parse_args()

ip_lookup = {
    'ldap1': 20,
    'ldap2': 21,
    'meta': 23,
    'lb': 24,
    'client': 25,
    'sandbox1': 26,
    'sbs': 27,
    'db': 28,
    'bhr': 29,
    'test': 30,
    'demo1': 31,
    'docker1': 32,
    'docker2': 33,
    'redis': 98,
    'mail': 99,
}

if args.ci and args.container:
    raise ValueError("Cannot generate a docker-compose.yml file for both CI and SCZ")
elif args.ci and not args.container:
    hosts = ['docker1', 'test']
elif not args.ci and args.container:
    hosts = ['bhr', 'client', 'mail', 'lb', 'demo1', 'docker1', 'docker2']
else:  # classic, non-ci, non-containerized setup
    hosts = ['bhr', 'client', 'lb', 'redis', 'mail', 'sandbox1', 'db', 'sbs', 'ldap1', 'ldap2', 'meta', 'demo1']

hosts_ip = {h: ip_lookup[h] for h in hosts}

# these are the Docker containers that need to be spun up
hosts = {
    'bhr': 29,
    'demo1': 31,
    'docker1': 32,
    'docker2': 33,
}

# the old non-containerized setup needs more hosts
if args.ci:
    hosts.update({
        'test': 30,
    })
else:
    hosts.update({
        'lb': 24,
        'client': 25,
    })
    if not args.container:
        hosts.update({
            'ldap1': 20,
            'ldap2': 21,
            'meta': 23,
            'sandbox1': 26,
            'sbs': 27,
            'db': 28,
        })

# these are the hostnames of virtual hosts on the load balancer
logical_hosts = [
    'sbs', 'ldap', 'meta',
    'oidc-op', 'sandbox1', 'pam',
    'demo1'
]

subnet = '172.20.1'
domain = 'scz-vm.net'


# generates config for a single host
def host_config(num: int, name: str) -> Dict[str, Any]:
    """
    Generate the config for a single host
    :param num: the last number of the IP address
    :param name: the hostname
    :return: the config for the host
    """
    data: Dict[str, Any] = {
        'image': 'scz-base',
        'hostname': name,
        'volumes': ['./ansible_key.pub:/tmp/authorized_keys'],
        'tmpfs': ['/run', '/run/lock', '/tmp'],
        'privileged': True,
        'security_opt': ['seccomp:unconfined', 'apparmor:unconfined'],
        'cap_add': ['SYS_ADMIN', 'SYS_PTRACE'],
        'networks': {
            'scznet': {
                'ipv4_address': f'{subnet}.{num}',
                'aliases': [f'{name}.vm.{domain}']
            }
        },
        'healthcheck': {
            'test': ['CMD', '/usr/bin/test', '!', '-e', '/etc/nologin'],
            'interval': '5s',
            'timeout': '1s',
            'retries': 1,
            'start_period': '0s'
        }
    }

    if not args.ci:
        data['extra_hosts'] = [f'{h}.{domain}:{subnet}.{hosts["lb"]}' for h in logical_hosts]

    if args.ci:
        data['volumes'] += ['../ci-runner:/tmp/ci-runner']

    return data


def mail_config(num: int, name: str) -> Dict[str, Any]:
    """
    Generate the config for the mail host
    :param num: the last number of the IP address
    :param name: the hostname
    :return: the config for the host
    """
    data = host_config(num, name)
    data.update({
        'image': 'axllent/mailpit',
        'ports': ['1025:1025', '8025:8025'],
    })
    return data


def redis_config(num: int, name: str) -> Dict[str, Any]:
    """
    Generate the config for the redis host
    :param num: the last number of the IP address
    :param name: the hostname
    :return: the config for the host
    """
    data = host_config(num, name)
    data.update({
        'image': 'bitnami/redis:latest',
        'ports': ['6379'],
        'environment': ['REDIS_PASSWORD=changethispassword']
    })
    return data


def create_compose() -> Dict[str, Any]:
    # generate the full docker-compose.yml file
    compose: Dict[str, Any] = dict()
    compose['networks'] = {
        'scznet': {
            'driver': 'bridge',
            'ipam': {
                'driver': 'default',
                'config': [{'subnet': f'{subnet}.0/24', 'gateway': f'{subnet}.1'}]
            },
            'driver_opts': {"com.docker.network.bridge.name": "br-sram"}
        }
    }
    compose['services'] = dict()
    for h, ip in hosts_ip.items():
        if h == 'mail':
            compose['services'][h] = mail_config(ip, h)
        elif h == 'redis':
            compose['services'][h] = redis_config(ip, h)
        else:
            compose['services'][h] = host_config(ip, h)

    if args.ci:
        # Add volume for docker '/var/lib/docker'
        compose.setdefault('volumes', {})['docker_volume'] = {'driver': 'local'}
        compose['services']['docker1'].setdefault('volumes', []).append('docker_volume:/var/lib/docker1')

    if args.container:
        # Add volume for docker '/var/lib/docker'
        compose.setdefault('volumes', {})['docker_volume'] = {'driver': 'local'}
        compose['services']['docker1'].setdefault('volumes', []).append('docker_volume:/var/lib/docker1')
        compose['services']['docker2'].setdefault('volumes', []).append('docker_volume:/var/lib/docker2')

    # Add mail test host on .99
    return compose


def main():
    compose = create_compose()

    # dump the yaml
    print("---")
    print("# This file has been automatically generated.  DO NOT EDIT, CHANGES WILL BE LOST!")
    print("# yamllint disable")
    print(yaml.dump(compose))


if __name__ == '__main__':
    main()
