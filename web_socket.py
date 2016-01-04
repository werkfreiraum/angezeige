#!/usr/bin/env python2
import signal, sys
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from main import start
import threading, time
from chooser import choose

class DataServer(WebSocket):
    def handleConnected(self):
        print(" - Connection established!")
        print(" - Start Thread!")
        self.stopThread = False
        self.t = threading.Thread(target=lambda: start(self, program = DataServer.program))
        self.t.daemon = True
        self.t.start()
    
    def handleClose(self):
        print(" - Connection Closed!")
        self.stopThread = True

    def write(self, message):
        if self.stopThread:
            print(" - Stop Thread!")
            sys.exit()
        self.sendMessage(message)

def main():
    DataServer.program = choose()

    print("Starting WebSocket ...")
    server = SimpleWebSocketServer('localhost', 8000, DataServer)
    print("WebSocket Ready!")

    def close_sig_handler(signal, frame):
        print("\nClosing WebSocket ...")
        server.close()
        print("Bye!")
        sys.exit()
    
    signal.signal(signal.SIGINT, close_sig_handler)
    server.serveforever()

if __name__ == "__main__":
    main()
