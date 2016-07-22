#!/usr/bin/env python2
import signal
import os
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from programs import Program
from writer.base import WriterProxy


class DataServer(WebSocket):

    def handleConnected(self):
        print(" - Connection established!")
        print(" - Start Thread!")
        Program.raiseException = True
        WriterProxy.instance = self
        self.t = Program.get_promoted_programs()["ShowTime"]()
        self.t.start()

    def handleClose(self):
        print(" - Connection Closed!")
        self.t.stop()
        self.t.join()

    def write(self, message):
        self.sendMessage(message)

    def close(self):
        pass


def main():
    print("Starting WebSocket ...")
    server = SimpleWebSocketServer('localhost', 8000, DataServer)
    print("WebSocket Ready!")
    print("Open " + os.path.dirname(os.path.realpath(__file__)) + "/simulation/index.html in you brower.")

    def close_sig_handler(signal, frame):
        print("\nClosing WebSocket ...")
        server.close()
        print("Bye!")
        exit()

    signal.signal(signal.SIGINT, close_sig_handler)
    server.serveforever()

if __name__ == "__main__":
    main()
