import os
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from writer.base import Writer
import logging
from threading import Thread
import time
import sys


class WebSocketWriter(Writer):
    server = None
    thread = None
    instances = []
    last_message = ''

    class WebSocketWriterSocket(WebSocket):

        # def __init__(self, server, sock, address):
        #    WebSocket.__init__(self, server, sock, address)

        def handleConnected(self):
            logging.debug(" - Connection established!")
            WebSocketWriter.instances.append(self)
            self.write(WebSocketWriter.last_message)

        def handleClose(self):
            logging.debug(" - Connection Closed!")
            WebSocketWriter.instances.remove(self)

        def write(self, message):
            self.sendMessage(message)

        # def close(self):
        #    pass

    def __init__(self, port=8000, bind_address='localhost'):
        self.port = port
        self.bind_address = bind_address
        self.thread = Thread(name="WebSocketServer", target=self._serve)
        self.thread.start()

    def _serve(self):
        logging.debug("Starting WebSocket (Port: " + str(self.port) + ", Bind Address: " + self.bind_address + ")...")
        self.server = SimpleWebSocketServer(self.bind_address, self.port, self.WebSocketWriterSocket, selectInterval=0.1)
        logging.debug("WebSocket Ready!")
        logging.debug("Open " + os.path.dirname(os.path.realpath(__file__)) + "/simulation/index.html in you brower.")
        try:
            self.server.serveforever()
        except Exception as e:
            logging.exception(e)

        logging.debug("WebSocket Closed!")
        sys.exit()

    def write(self, message):
        WebSocketWriter.last_message = message
        for i in self.instances:
            i.write(message)

    def close(self):
        logging.debug("Closing WebSocket ...")
        self.server.close()
        logging.debug("Bye!")
        if self.thread.is_alive():
            #logging.debug("DO SOMETHING STUPID")
            #self.server.listeners = None
            #logging.debug("WAITING FOR THREAD!")
            self.thread.join()
