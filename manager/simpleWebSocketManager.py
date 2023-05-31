from misc.simpleWebSocketBase import WebSocketBase, WebSocketBaseSocket
from manager.base import Manager
import logging
import json


class SimpleWebSocketManagerSocket(WebSocketBaseSocket):
    def handleConnected(self):
        pass

    def handleMessage(self):
        self.sendMessage(json.dumps(self.server.base.do(json.loads(self.data))))


class SimpleWebSocketManager(WebSocketBase, Manager):
    last_message = ''
    socket_imp_class = SimpleWebSocketManagerSocket

    def __init__(self, port=8001, bind_address='localhost'):
        Manager.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)


