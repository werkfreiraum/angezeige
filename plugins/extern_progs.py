# -*- coding: utf-8 -*-
import logging
from programs import Program
import logging


class ExternAngezeige(Program):
    websocket = None
    timeout = 1

    def __init__(self, uri_websocket):
        Program.__init__(self)
        self.uri_websocket = uri_websocket

    def open(self):
        global WebSocketTimeoutException
        from websocket import create_connection, WebSocketTimeoutException
        self.websocket = create_connection(self.uri_websocket, timeout=self.timeout)

    def do(self):
        while True:
            try:
                message = self.websocket.recv()
                self.writer.write(message)
            except WebSocketTimeoutException as e:
                pass
            
            self.wait(0)

    def close(self):
        logging.debug('ExternAngezeige.close')
        if self.websocket:
            self.websocket.close()

    @staticmethod
    def get_params():
        params = {}
        params['uri_websocket'] = "ws://foosball.local:5005"
        return params
