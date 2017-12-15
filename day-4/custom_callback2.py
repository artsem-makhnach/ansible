from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

from ansible import constants as C
from ansible.plugins.callback.default import CallbackModule as CallbackModule_default
from ansible.utils.color import colorize, hostcolor

def _color(play):
    if play._result.get('failed'):
        return C.COLOR_ERROR
    if play._result.get('changed'):
        return C.COLOR_CHANGED
    if play._result.get('skipped'):
        return C.COLOR_SKIP
    return 'green'

def _status(play):
    if play._result.get('failed'):
        return 'failed'
    if play._result.get('changed'):
        return 'changed'
    if play._result.get('skipped'):
        return 'skipped'
    return 'ok'

def _parse_flags(play):
   flags = {}
   try:
       name = play._task.name.split(' ')
   except AttributeError as e:
       return flags
   for s in name:
       f = s.split('=')
       if len(f) == 2:
           flags[f[0]] = f[1]
   return flags


class CallbackModule(CallbackModule_default):

    ''' when pretty_output is in a task name, output both the stdout and the stderr to the console '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'improved'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):
        self._play = None
        self._last_task_banner = None
        super(CallbackModule, self).__init__()

    def _pretty(self, play):
        self._display.display('{0}: [{1}]'.format(_status(play), play._host.name), color=_color(play))

        stdout = play._result.get('stdout', '\n'.join(play._result.get('stdout_lines', [])))
        if stdout:
            self._display.display('--- stdout ---', color='blue')
            self._display.display(stdout, color='blue')

        stderr = play._result.get('stderr', '')
        if stderr:
            self._display.display('--- stderr ---', color='red')
            self._display.display(stderr, color='red')

    def _skip(self, play, **kwargs):
        if play._result.get('skipped'):
            return
        task = sys._getframe(2).f_code.co_name
        getattr(super(CallbackModule, self), task)(play, **kwargs)

    def _output(self, play, **kwargs):
        flags = _parse_flags(play)
        if 'output' in flags and not self._display.verbosity:
            try:
                getattr(self, '_' + flags['output'])(play)
            except AttributeError as e:
                self._display.display(e, color='magenta')
                task = sys._getframe(1).f_code.co_name
                getattr(super(CallbackModule, self), task)(play, **kwargs)
        else:
            task = sys._getframe(1).f_code.co_name
            getattr(super(CallbackModule, self), task)(play, **kwargs)

    def v2_runner_on_failed(self, play, **kwargs):
        self._output(play, **kwargs)

    def v2_runner_on_ok(self, play, **kwargs):
        self._output(play, **kwargs)

    def v2_runner_on_skipped(self, play, **kwargs):
        self._output(play, **kwargs)

    def v2_runner_item_on_skipped(self, play, **kwargs):
        self._output(play, **kwargs)







from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
from datetime import datetime
from colorama import *

init()


class CallbackModule(CallbackBase):

    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'custom_callback'

    def __init__(self):

        super(CallbackModule, self).__init__()

        self.start_time = datetime.now()

    def days_hours_minutes_seconds(self, runtime):
        minutes = (runtime.seconds // 60) % 60
        r_seconds = runtime.seconds - (minutes * 60)
        return runtime.days, runtime.seconds // 3600, minutes, r_seconds

    def v2_playbook_on_stats(self, stats):
        end_time = datetime.now()
        runtime = end_time - self.start_time
        self._display.display("Playbook run took %s days, %s hours, %s minutes, %s seconds" % (self.days_hours_minutes_seconds(runtime)))

    def show(self, task, host, result, caption):
        buf = "{0} | {1} | {2} | rc={3} >>\n".format(task, host, caption, result.get('rc', 'n/a'))
        buf += result.get('stdout', '')
        buf += result.get('stderr', '')
        buf += result.get('msg', '')
        print(buf + "\n")


    # def v2_playbook_on_start(self, playbook):
    #     self.show("Test")
    #
    def v2_runner_on_failed(self, result, ignore_errors=False):
         self.show(result._task, result._host.get_name(), result._result, "FAILED")

    def v2_runner_on_ok(self, result):
         self.show(result._task, result._host.get_name(), result._result, Fore.BLUE+"OK")

    def v2_runner_on_skipped(self, result):
         self.show(result._task, result._host.get_name(), result._result, "SKIPPED")

    def v2_runner_on_unreachable(self, result):
         self.show(result._task, result._host.get_name(), result._result, "UNREACHABLE")