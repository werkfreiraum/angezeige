#!/bin/python2
import signal, sys
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from main import run
import threading, time

class DataServer(WebSocket):
    def handleConnected(self):
        self.t = threading.Thread(target=lambda: run(self.write_socket, output_format="hex"))
        self.t.daemon = True
        self.t.start()
    
    def handleClose(self):
        self.t._stop()

    def write_socket(self, message):
        self.sendMessage(unicode(message))

def main():
    print("Starting WebSocket ...")
    server = SimpleWebSocketServer('localhost', 8000, DataServer)
    print("Ready!")

    def close_sig_handler(signal, frame):
        print("\nClosing WebSocket ...")
        server.close()
        print("Bye!")
        sys.exit()
    
    signal.signal(signal.SIGINT, close_sig_handler)
    server.serveforever()

if __name__ == "__main__":
    main()
