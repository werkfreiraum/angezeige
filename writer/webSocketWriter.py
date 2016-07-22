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
    class WebSocketWriterSocket(WebSocket):
        #
        #def __init__(self, server, sock, address):
        #    WebSocket.__init__(self, server, sock, address)

        def handleConnected(self):
            logging.debug(" - Connection established!")
            WebSocketWriter.instances.append(self)
            

        def handleClose(self):
            logging.debug(" - Connection Closed!")
            WebSocketWriter.instances.remove(self)

        def write(self, message):
            self.sendMessage(message)

        #def close(self):
        #    pass
            
    def __init__(self):
        self.thread = Thread(name="WebSocketServer", target=self._serve)
        self.thread.start()

    def _serve(self):
        logging.debug("Starting WebSocket ...")
        self.server = SimpleWebSocketServer('localhost', 8000, self.WebSocketWriterSocket, selectInterval = 0)
        logging.debug("WebSocket Ready!")
        logging.debug("Open " + os.path.dirname(os.path.realpath(__file__)) + "/simulation/index.html in you brower.")
        self.server.serveforever()
        logging.debug("WebSocket Closed!")
        sys.exit()


    def write(self, message):
        #pass
        logging.debug('---')
        for i in self.instances:
            logging.debug(i)
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
        