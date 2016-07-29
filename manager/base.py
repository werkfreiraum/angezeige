# -*- coding: utf-8 -*-
import logging
from programs import Program
from switches.base import SwitchProxy
from writer.base import WriterProxy

from proxy import Proxy

class Manager(object):
    def do(self, command):
        if command[u'code'] == u'switch':
            if command[u'subcode'] == u'next':
                SwitchProxy.instance.next()

        

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
