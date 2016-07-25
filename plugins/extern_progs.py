# -*- coding: utf-8 -*-
import logging
from programs import Program
import logging


class ExternAngezeige(Program):
    websocket = None
    timeout =2

    def __init__(self, uri_websocket):
        Program.__init__(self)
        self.uri_websocket = uri_websocket

    def open(self):
        from websocket import create_connection
        self.websocket = create_connection(self.uri_websocket, timeout=self.timeout)

    def do(self):
        while True:
            # TODO: THIS ONE IS BLOCKING
            message = self.websocket.recv()
            self.writer.write(message)
            self.wait(0)

    def close(self):
        if self.websocket:
            self.websocket.close()

    @staticmethod
    def get_params():
        params = {}
        params['uri_websocket'] = "ws://foosball.local:5005"
        return params
