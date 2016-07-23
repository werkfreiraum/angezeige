import json
from programs import Program

class Switch(object):
    detected = False
    forward = None

    def __init__(self, ret_func=None):
        self.ret_func = ret_func

    def set_forward(self, forward):
        self.forward = forward

    def start_detection(self):
        pass

    def close(self):
        pass

    def _detected(self, *args):
        self.detected = True
        if self.ret_func:
            self.ret_func(self)
        if self.forward:
            self.forward._detected()


class SwitchProxy(Switch):
    detected = False
    switches = {}
    switch_programs = []
    active_switch_program = -1;
    instance = None


    def __init__(self, switches, switch_programs_file = None):
        for uniqueId, info in switches.iteritems():
            switchType = info["type"]
            params = info["params"] if "params" in info else {}
            self.add_switch(uniqueId, switchType, params=params)

        #if len(switches) > 0:
        with open(switch_programs_file) as data_file:
            self.switch_programs = json.load(data_file)

        SwitchProxy.instance = self

    def add_switch(self, uniqueId, switchType, params={}):
        switch = globals()[switchType](**params)
        switch.set_forward(self)
        self.switches[uniqueId] = switch

    def start_detection(self):
        for s in self.switches:
            # if self.switches[s]['active']:
            self.switches[s].start_detection()

    def stop_detection(self):
        for s in self.switches:
            # if self.switches[s]['active']:
            s.stop_detection()

    def close(self):
        for s in self.switches:
            self.switches[s].close()

    def next(self):
        self.active_switch_program = (self.active_switch_program + 1)%len(self.switch_programs)
        return self.switch_programs[self.active_switch_program]

    def _detected(self):
        self.detected = True
        #if switch and switch.detected:
        Program.start_program(self.next())
        self.detected = False


from switches.clapSwitch import ClapSwitch
from switches.pinSwitch import PinSwitch