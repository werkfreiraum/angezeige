from misc.autobahnWebSocketBase import WebSocketBase, WebSocketBaseSocket
from manager.base import Manager
import logging
import json


class AutobahnWebSocketManagerSocket(WebSocketBaseSocket):

    def onMessage(self, message, isBinary):
        self.sendMessage(bytes(json.dumps(self.factory.base.do(json.loads(message))), 'ascii'))


class AutobahnWebSocketManager(WebSocketBase, Manager):
    socket_imp_class = AutobahnWebSocketManagerSocket

    def __init__(self, port=8003, bind_address='localhost'):
        Manager.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)

    #def broadcast(self, message):
    #    self.factory.broadcast(json.dumps(message))

    def update(self, info):
        self.factory.broadcast(json.dumps(info))
