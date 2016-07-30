from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import logging
from threading import Thread
import sys

class WebSocketBaseSocket(WebSocket):

    def handleConnected(self):
        logging.debug(type(self).__name__ + " - Connection established!")
        self.server.base.instances.append(self)

    def handleClose(self):
        logging.debug(type(self).__name__ + " - Connection Closed!")
        if self in self.server.base.instances:
            self.server.base.instances.remove(self)


class WebSocketBaseServer(SimpleWebSocketServer):

    def __init__(self, base):
        SimpleWebSocketServer.__init__(self, base.bind_address, base.port, base.socket_imp_class, selectInterval=0.1)
        self.base = base


class WebSocketBase(object):
    def __init__(self, port, bind_address):
        self.port = port
        self.bind_address = bind_address
        self.instances = []

    def enable(self):
        self.thread = Thread(name=type(self).__name__, target=self._serve)
        self.thread.start()

    def _serve(self):
        logging.debug("Starting " + type(self).__name__ + " (Port: " +
                      str(self.port) + ", Bind Address: '" + self.bind_address + "')...")
        self.server = WebSocketBaseServer(self)
        logging.debug(type(self).__name__ + " Ready!")

        try:
            self.server.serveforever()
        except Exception as e:
            logging.exception(e)

        logging.debug(type(self).__name__ + " Closed!")
        sys.exit()

    def disable(self):
        logging.debug("Closing " + type(self).__name__ + " ...")
        self.server.close()
        logging.debug("Closed " + type(self).__name__)
        if self.thread.is_alive():
            #logging.debug("DO SOMETHING STUPID")
            #self.server.listeners = None
            #logging.debug("WAITING FOR THREAD!")
            self.thread.join()
