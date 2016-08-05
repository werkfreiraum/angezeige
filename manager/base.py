# -*- coding: utf-8 -*-
import logging
from programs import Program
from switches.base import SwitchProxy
from writer.base import WriterProxy
from misc.proxy import Proxy

api_methods = {}
class Manager(object):

    @staticmethod
    def error(message):
        return {'valid': False, 'error': message}

    def do(self, command):
        if 'name' in command:
            if command['name'] in api_methods:
                params = command['params'] if 'params' in command else {}
                return api_methods[command['name']](self, **params)
            else:
                return self.error("Command not implemented!")
        else:
            return self.error("No function name provided!")

    def api_method(func):
        def wrapper(*args, **kwargs):
            ret = {}
            try:
                info = func(*args, **kwargs)
                if info:
                    ret['info'] = info
            except Exception as e:
                return Manager.error(str(e))
            ret['valid'] = True
            return ret
        api_methods[func.__name__] = wrapper
        return func

    @api_method
    def get_programs(self):
        programs = Program.get_promoted_programs()
        info = {}
        for p in programs:
            info[p] = programs[p].get_params()
        return info

    @api_method
    def switch(self):
        SwitchProxy.instance.next()

    @api_method
    def start_program(self, **info):
        Program.start(**info)


class ManagerProxy(Proxy, Manager):

    @staticmethod
    def get_imp_class(name):
        return globals()[name]

    def is_urwid_enabled(self):
        for manager in self.enabled_items:
            if type(self.items[manager]) is UrwidManager:
                return True
        return False


from manager.urwidManager import UrwidManager
from manager.simpleWebSocketManager import SimpleWebSocketManager
from manager.autobahnWebSocketManager import AutobahnWebSocketManager
