# -*- coding: utf-8 -*-
import logging

from programs import Program
from .url_progs import JsonReader


URL = "http://rubinstein.local/api/"
# PARAMTERS = {
#     'job': [
#         'progress.completion',
#         #'job.estimatedPrintTime',  # TODO should convert to hh:mm
#     ]
# }


class RubinsteinProgress(JsonReader):
    name = "RUPR"
    
    def __init__(self, color=None):
        refresh_duration = 5
        path = "progress.completion"
        JsonReader.__init__(self, color=color, uri="pospone", refresh_duration=refresh_duration, path=path)

    def open(self):
        uri = "{}{}?apikey={}".format(URL, "job", self.get_api_key['rubinstein'])
        self.setUri(uri)

    def getMessage(self):
        rawMessage = JsonReader.getMessage(self)
        logging.debug("RubinsteinProgress: " + rawMessage)
        message = int(round(rawMessage))
        if message == 100:
            return "finished!"
        else:
            return str(message).rjust(2) + u"°o"

    @staticmethod
    def get_params():
        return Program.get_params()
