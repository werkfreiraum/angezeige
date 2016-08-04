from misc.autobahnWebSocketBase import WebSocketBase, WebSocketBaseSocket
from manager.base import Manager
import logging
import json


class AutobahnWebSocketManagerSocket(WebSocketBaseSocket):

    def onConnected(self, request):
        pass

    def onMessage(self, message, isBinary):
        command = json.loads(message)
        #logging.debug(command)
        #print("do: " + str(command))
        back = self.factory.base.do(command)
        #print("done: " + str(back))
        self.sendMessage(json.dumps(back))


class AutobahnWebSocketManager(WebSocketBase, Manager):
    socket_imp_class = AutobahnWebSocketManagerSocket

    def __init__(self, port=8003, bind_address='localhost'):
        Manager.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)