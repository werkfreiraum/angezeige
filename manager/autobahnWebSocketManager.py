from misc.autobahnWebSocketBase import WebSocketBase, WebSocketBaseSocket
from manager.base import Manager
import logging
import json


class AutobahnWebSocketManagerSocket(WebSocketBaseSocket):

    def onConnected(self, request):
        pass

    def onMessage(self, message, isBinary):
        self.sendMessage(json.dumps(self.factory.base.do(json.loads(message))))


class AutobahnWebSocketManager(WebSocketBase, Manager):
    socket_imp_class = AutobahnWebSocketManagerSocket

    def __init__(self, port=8003, bind_address='localhost'):
        Manager.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)