from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
from datetime import datetime
from colorama import *

#init()

log = open("log.txt", "w")


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

    def show(self, task, host, result, caption):
        buf = "{0} | {1} | {2} | rc={3} >>\n".format(task, host, caption, result.get('rc', 'n/a'))
        buf += result.get('stdout', '')
        buf += result.get('stderr', '')
        buf += result.get('msg', '')
        print(Fore.RED+buf[:5]+Fore.LIGHTCYAN_EX+buf[5:] + "\n")

        log.writelines(buf+"\n")


    # def v2_playbook_on_start(self, result):
    #     print (result._host)

    def v2_playbook_on_stats(self, stats):
        end_time = datetime.now()
        runtime = end_time - self.start_time
        result = "Playbook run took %s days, %s hours, %s minutes, %s seconds" % (self.days_hours_minutes_seconds(runtime))
        self._display.display(Fore.LIGHTMAGENTA_EX+"Playbook run took %s days, %s hours, %s minutes, %s seconds" % (self.days_hours_minutes_seconds(runtime)))
        log.writelines(result + "\n")

    def v2_runner_on_failed(self, result, ignore_errors=False):
         self.show(result._task, result._host.get_name(), result._result, "FAILED")

    def v2_runner_on_ok(self, result):
         self.show(result._task, result._host.get_name(), result._result, "OK")

    def v2_runner_on_skipped(self, result):
         self.show(result._task, result._host.get_name(), result._result, "SKIPPED")

    def v2_runner_on_unreachable(self, result):
         self.show(result._task, result._host.get_name(), result._result, "UNREACHABLE")
