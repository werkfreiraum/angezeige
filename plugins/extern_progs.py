# -*- coding: utf-8 -*-
import logging
from programs import Program
import logging

URI_WEBSOCKET = "ws://localhost:8001"


class ExternAngezeige(Program):

    def __init__(self, websocket=None):
        Program.__init__(self)
        from websocket import create_connection
        self.websocket = create_connection(websocket)

    def do(self):
        while True:
            message = self.websocket.recv()
            self.writer.write(message)
            self.wait(0)

    @staticmethod
    def get_params():
        params = {}
        params['websocket'] = URI_WEBSOCKET
        return params