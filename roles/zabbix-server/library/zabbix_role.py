#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: zabbix_role
https://www.zabbix.com/documentation/current/en/manual/api/reference/role
https://www.zabbix.com/documentation/current/en/manual/api/reference/role/create

short_description: Adds or removes zabbix roles

description: This module adds or removes zabbix roles

options:
    server_url: http://localhost/zabbix
    login_user: username
    login_password: password
    state: exact
    name: Operators
      The name of the role
    type: 1
      https://www.zabbix.com/documentation/current/en/manual/api/reference/role/object#role
    rules:
      https://www.zabbix.com/documentation/current/en/manual/api/reference/role/object#role-rules

author:
    - Martin van Es
'''

EXAMPLES = r'''
# Creat role Operators with ui elements monitoring.hosts
# disabled and monitoring.maps enabled

- name: Create Zabbix role
  local_action:
    module: zabbix_role
    server_url: http://zabbix.scz-vm.net/
    login_user: username
    login_password: login_password
    state: present
    name: Operators
    type: 1
    rules:
      ui:
        name: "monitoring.hosts"
        status: 0
        name: "monitoring.maps"
        status: 1
'''

RETURN = r'''
# Return values
msg:
    description: The result of the action
    type: str
    returned: always
    sample: 'No action'
changed:
    description: The consequence of the action
    type: bool
    returned: always
    sample: False
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

try:
    from zabbix_api import ZabbixAPI

    HAS_ZABBIX_API = True
    ZBX_IMP_ERR = Exception()
except ImportError:
    ZBX_IMP_ERR = traceback.format_exc()
    HAS_ZABBIX_API = False


def find_val(outval, inval):
    if outval == str(inval):
        return True
    return False


def find_list(outval, inval):
    if set(outval) == set(inval):
        return True
    return False


def find_dict(outval, inval):
    for out in outval:
        m = True
        for k, v in inval.items():
            if out[k] == str(v):
                continue
            else:
                m = False
        if m:
            break
    return m


def equal(inp, out):
    verdict = True
    for rule, value in inp.items():
        if not isinstance(value, list):
            verdict = verdict and find_val(out.get(rule, ''), value)
        else:
            if len(value):
                if not isinstance(value[0], dict):
                    verdict = verdict and find_list(out.get(rule, []), value)
                else:
                    for v in value:
                        verdict = verdict and find_dict(out.get(rule, {}), v)
            else:
                verdict = verdict and find_list(rule, value)
    return verdict


def run_module():
    # seed the result dict in the object
    changed = False
    msg = "No action"

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type='str', required=True),
        login_user=dict(type='str', required=True),
        login_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', required=False, default='present'),
        name=dict(type='str', required=True),
        type=dict(type='int', required=False, default=1),
        rules=dict(type='dict', required=True),
    )

    # the AnsibleModule object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not HAS_ZABBIX_API:
        module.fail_json(msg=missing_required_lib(
            'zabbix-api', url='https://pypi.org/project/zabbix-api/'), exception=ZBX_IMP_ERR)

    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    state = module.params['state']
    name = module.params['name']
    type = module.params['type']
    rules = module.params['rules']

    # This may help with debugging as print() will not work
    # raise Exception(rules)

    # the Zabbix api object
    zapi = ZabbixAPI(server_url)
    zapi.login(user=login_user, password=login_password)

    msg = zapi.role.get({
        "output": "extend",
        "selectRules": "extend",
        "filter": {"name": name}
    })

    if msg:
        if len(msg) == 1:
            r = msg[0]
            if r['readonly'] != 1:
                roleid = r['roleid']
                if state == 'absent':
                    msg = zapi.role.delete([f"{roleid}"])
                    changed = True
                    msg = "Role deleted"
                else:
                    if not equal(rules, r['rules']):
                        msg = zapi.role.update({"roleid": roleid, "rules": rules})
                        changed = True
                        msg = "Role updated"
        else:
            module.fail_json(msg='Too many role matches', exception=ZBX_IMP_ERR)
    else:
        msg = zapi.role.create({
            "name": name,
            "type": type,
            "rules": rules
        })
        changed = True
        msg = "Role created"

    zapi.logout()

    module.exit_json(msg=msg, changed=changed)


def main():
    run_module()


if __name__ == '__main__':
    main()
