from misc.simpleWebSocketBase import WebSocketBase, WebSocketBaseSocket
from writer.base import Writer
import logging
from threading import Thread
import binascii

class SimpleWebSocketWriterSocket(WebSocketBaseSocket):

    def handleConnected(self):
        WebSocketBaseSocket.handleConnected(self)
        self.sendMessage(self.server.base.last_message)

    def sendMessage(self, message):
        #print("sendMessage")
        WebSocketBaseSocket.sendMessage(self, unicode(binascii.hexlify(message)))
        print("sendMessage" + str(binascii.hexlify(message)))


class SimpleWebSocketWriter(WebSocketBase, Writer):
    socket_imp_class = SimpleWebSocketWriterSocket

    def __init__(self, port=8000, bind_address='localhost'):
        Writer.__init__(self)
        WebSocketBase.__init__(self, port, bind_address)

    def write(self, message):
        self.last_message = message
        for i in self.instances:
            i.sendMessage(message)
