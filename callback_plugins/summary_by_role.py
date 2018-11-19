from __future__ import (absolute_import, division, print_function)
from six import iteritems
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
#from ansible.executor.task_result import TaskResult
import json


class CallbackModule(CallbackBase):
    """
    This callback module tells you per role how many ok/skipped/changed tasks tere were
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'summary_by_role'

    # only needed if you ship it and don't want to enable by default
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):
        super(CallbackModule, self).__init__()
        self._stats = {}

    def v2_runner_on_skipped(self, result):
        self._handle_result(result)

    def v2_runner_on_ok(self, result):
        self._handle_result(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._handle_result(result)

    def v2_runner_on_unreachable(self, result):
        self._handle_result(result)

    def _handle_result(self, result):
        if result.is_skipped():
            status = 'skipped'
        elif result.is_failed() or result.is_unreachable():
            status = 'failed'
        elif result.is_changed():
            status = 'changed'
        else:
            status = 'ok'
        role = result._task._role
        self._inc_stats(role.get_name() if role else '_', status)

    def _inc_stats(self, role, status):
        if status not in ['skipped', 'failed', 'changed', 'ok']:
            raise Exception("Unknown status '{}'".format(status))
        if role not in self._stats:
            self._stats[role] = {'skipped': 0, 'failed': 0, 'changed': 0, 'ok': 0}
        self._stats[role][status] += 1

    def v2_playbook_on_stats(self, stats):
        # display on screen
        self._display.display("=================================================================")
        self._display.display("Statistics overview:")
        self._display.display("{:<20} {:>7} {:>7} {:>7} {:>7}".format(
            'Role', 'skipped', 'ok', 'changed', 'failed')
        )
        for k, v in iteritems(self._stats):
            self._display.display("{:<20} {:>7} {:>7} {:>7} {:>7}".format(
                k, v['skipped'], v['ok'], v['changed'], v['failed'])
            )
        self._display.display("=================================================================")

        # write to file
        with open('provision_status.json', 'w') as f:
            json.dump(self._stats, f, indent=4)
