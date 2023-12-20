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
parser.add_argument('--ci', action='store_true', help='generate a docker-compose.yml file for CI')
parser.add_argument('--container', action='store_true', help='generate a docker-compose.yml file for SCZ')
args = parser.parse_args()

# these are the Docker containers that need to be spun up
hosts = {
    'lb': 24,
    'client': 25,
    'bhr': 29,
    'docker': 31,
}

# the old non-containerized setup needs more hosts
if not args.container:
    hosts.update({
        'ldap1': 20,
        'ldap2': 21,
        'meta': 23,
        'sandbox1': 26,
        'sbs': 27,
        'db': 28,
    })

if args.ci:
    hosts.update({
        'test': 30,
    })

# these are the hostnames of virtual hosts on the load balancer
logical_hosts = [
    'sbs', 'ldap', 'meta',
    'oidc-op', 'sandbox1', 'pam'
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
        if name == 'sbs':
            data.update({
                'depends_on': ['db', 'redis', 'test'],
                'volumes': ['../ci-runner:/tmp/ci-runner'],
            })

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
        'image': 'mailhog/mailhog:v1.0.1',
        'ports': ['80:8025'],

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
    compose['version'] = '2.4'
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
    compose['services'] = {h: host_config(ip, h) for h, ip in hosts.items()}

    # Add redis host on .98
    if not args.container:
        compose['services']['redis'] = redis_config(98, 'redis')

    # Add mail test host on .99
    if not args.ci:
        compose['services']['mail'] = mail_config(99, 'mail')
        # Add volume for docker '/var/lib/docker'
        compose.setdefault('volumes', {})['docker_volume'] = {'driver': 'local'}
        compose['services']['docker'].setdefault('volumes', []).append('docker_volume:/var/lib/docker')

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
