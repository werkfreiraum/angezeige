# -*- coding: utf-8 -*-
import logging
from programs import Program
from switches.base import SwitchProxy
from writer.base import WriterProxy
from misc.proxy import Proxy


api_methods = {}


class Manager(object):
    def update(self, info):
        pass

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
    def get_status(self):
        info = {}
        info['program'] = {}
        info['program']['status'] = 'stopped'
        if Program.running:
            info['program']['status'] = 'running'
            info['program']['name'] = type(Program.running).__name__

            e = Program.running.error()
            if e:
                info['program']['status'] = 'error'
                info['program']['error'] = {
                    'class': type(e).__name__,
                    'text': str(e)
                }

        info['switch'] = SwitchProxy.instance.detected

        return info

    @api_method
    def get_programs(self):
        programs = Program.get_promoted_programs()
        info = {}
        for p in programs:
            info[p] = programs[p].get_params()
        return info

    @api_method
    def get_environment(self):
        info = {}

        for proxy_name, proxy_class in proxyClasses.iteritems():
            info[proxy_name] = []
            for item in proxy_class.instance.items:
                info[proxy_name].append({
                    'name': item,
                    'enabled': proxy_class.instance.is_enabled(item),
                    'params': proxy_class.instance.params[item]
                })

        return info

    @api_method
    def set_environment(self, proxy, name, state):
        if state:
            proxyClasses[proxy].instance.enable(name)
        else:
            proxyClasses[proxy].instance.disable(name)

        info = {
                'type': 'update',
                'class': 'environment',
                'info': {
                    'proxy': proxy,
                    'name': name,
                    'enabled': state
                }
            }

        for m in ManagerProxy.instance.items.values():
            m.update(info)

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

proxyClasses = {
    "Switches": SwitchProxy,
    "Writer": WriterProxy,
    "Manager": ManagerProxy
}
