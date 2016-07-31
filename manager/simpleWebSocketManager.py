from misc.simpleWebSocketBase import WebSocketBase, WebSocketBaseSocket
from manager.base import Manager
import logging
from threading import Thread
import json


class SimpleWebSocketManagerSocket(WebSocketBaseSocket):

    def handleConnected(self):
        #self.sendMessage(unicode(json.dumps(['hallo'])))
        #self.sendMessage(u'hallo')
        pass

    def handleMessage(self):
        command = json.loads(self.data)
        #logging.debug(command)
        #print("do: " + str(command))
        back = self.server.base.do(command)
        #print("done: " + str(back))
        self.sendMessage(unicode(json.dumps(back)))


class SimpleWebSocketManager(WebSocketBase, Manager):
    last_message = ''
    socket_imp_class = SimpleWebSocketManagerSocket

    def __init__(self, port=8001, bind_address='localhost'):
        Manager.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)


