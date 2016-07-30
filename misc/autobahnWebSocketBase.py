from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import logging
from threading import Thread
import sys
from twisted.internet import reactor



class WebSocketBaseSocket(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        pass
        # if isBinary:
        #     print("Binary message received: {0} bytes".format(len(payload)))
        # else:
        #     print("Text message received: {0}".format(payload.decode('utf8')))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class WebSocketBaseServer(WebSocketServerFactory):

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, msg):
        for c in self.clients:
            c.sendMessage(msg)


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

        self.factory = WebSocketBaseServer(unicode("ws://" + self.bind_address + ":" + str(self.port)))
        self.factory.protocol = self.socket_imp_class

        reactor.listenTCP(self.port, self.factory)

        try:
            reactor.run(installSignalHandlers=False)
        except Exception as e:
            logging.exception(e)

        logging.debug("Closed " + type(self).__name__)
        sys.exit()

    def disable(self):
        logging.debug("Closing " + type(self).__name__ + " ...")
        reactor.callFromThread(lambda: reactor.stop())
        #reactor.stop()
        #self.server.close()
        #logging.debug("Closed " + type(self).__name__)
        if self.thread.is_alive():
            #logging.debug("DO SOMETHING STUPID")
            #self.server.listeners = None
            #logging.debug("WAITING FOR THREAD!")
            self.thread.join()
