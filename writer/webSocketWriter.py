from SimpleWebSocketServer import WebSocket
from webSocketBase import WebSocketBase, WebSocketBaseSocket
from writer.base import Writer
import logging
from threading import Thread


class WebSocketWriterSocket(WebSocketBaseSocket):

    def handleConnected(self):
        WebSocketBaseSocket.handleConnected(self)
        self.sendMessage(self.server.base.last_message)


class WebSocketWriter(WebSocketBase, Writer):
    socket_imp_class = WebSocketWriterSocket

    def __init__(self, port=8000, bind_address='localhost'):
        Writer.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)

    def write(self, message):
        self.last_message = message
        for i in self.instances:
            i.sendMessage(message)
