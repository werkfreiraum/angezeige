from misc.autobahnWebSocketBase import WebSocketBase, WebSocketBaseSocket
from writer.base import Writer
import logging
from threading import Thread
import binascii


class AutobahnWebSocketWriterSocket(WebSocketBaseSocket):

    def onConnected(self, request):
        WebSocketBaseSocket.onConnected(self, request)
        self.sendMessage(self.factory._last_message)

    def sendMessage(self, message):
        WebSocketBaseSocket.sendMessage(self, binascii.hexlify(message))


class AutobahnWebSocketWriter(WebSocketBase, Writer):
    socket_imp_class = AutobahnWebSocketWriterSocket

    def __init__(self, port=8000, bind_address='localhost'):
        Writer.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)

    def write(self, message):
        self.factory._last_message = message
        self.factory.broadcast(message)
