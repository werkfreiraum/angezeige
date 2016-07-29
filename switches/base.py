import json
from programs import Program
from proxy import Proxy


class Switch(object):
    detected = False
    forward = None

    def __init__(self, ret_func=None):
        self.ret_func = ret_func

    def set_forward(self, forward):
        self.forward = forward

    def enable(self):
        pass

    def disable(self):
        pass

    def _detected(self, *args):
        self.detected = True
        if self.ret_func:
            self.ret_func(self)
        if self.forward:
            self.forward._detected()


class SwitchProxy(Proxy, Switch):
    detected = False
    switch_programs = []
    active_switch_program = -1

    def __init__(self, items, switch_programs_file=None):
        Proxy.__init__(self, items)
        Switch.__init__(self)

        with open(switch_programs_file) as data_file:
            self.switch_programs = json.load(data_file)

        for switch in self.items:
            self.items[switch].set_forward(self)

    def next(self):
        self.active_switch_program = (self.active_switch_program + 1) % len(self.switch_programs)
        Program.start(self.switch_programs[self.active_switch_program])

    def _detected(self, *args):
        self.detected = True
        self.next()
        self.detected = False

    @staticmethod
    def get_imp_class(name):
        return globals()[name]


from switches.clapSwitch import ClapSwitch
from switches.pinSwitch import PinSwitch
