# -*- coding: utf-8 -*-
import logging
from programs import Program
from switches.base import SwitchProxy
from writer.base import WriterProxy
from misc.proxy import Proxy


class Manager(object):

    def do(self, command):
        logging.debug(command)
        
        if command[u'code'] == u'switch':
            if command[u'subcode'] == u'next':
                SwitchProxy.instance.next()
                return self.success()

        if command[u'code'] == u'info':
            if command[u'subcode'] == u'programs':
                return self.success({'programs': Program.get_promoted_programs().keys()})

    def success(self, info = None):
        ret = {}
        if info:
            ret[info] = info
        info['valid'] = True
        return info


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
from manager.webSocketManager import WebSocketManager
