from SimpleWebSocketServer import WebSocket
from webSocketBase import WebSocketBase, WebSocketBaseSocket
from manager.base import Manager
import logging
from threading import Thread
import json


class WebSocketManagerSocket(WebSocketBaseSocket):

    def handleConnected(self):
        self.sendMessage(unicode(json.dumps(['hallo'])))
        #self.sendMessage(u'hallo')

    def handleMessage(self):
        command = json.loads(self.data)
        logging.debug(command)
        self.server.base.do(command)


class WebSocketManager(WebSocketBase, Manager):
    last_message = ''
    socket_imp_class = WebSocketManagerSocket

    def __init__(self, port=8001, bind_address='localhost'):
        Manager.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)


