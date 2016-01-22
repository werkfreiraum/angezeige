# -*- coding: utf-8 -*-
import json
import urllib2
import re
import logging
from contextlib import closing

from private import api_keys
from programs import Program
from url_progs import JsonReader


URL = "http://rubinstein.local/api/"
# PARAMTERS = {
#     'job': [
#         'progress.completion',
#         #'job.estimatedPrintTime',  # TODO should convert to hh:mm
#     ]
# }


class RubinsteinProgress(JsonReader):

    def __init__(self, writer=None, color=None):
        uri = "{}{}?apikey={}".format(URL, "job", api_keys['rubinstein'])
        refresh_duration = 5
        path = "progress.completion"
        JsonReader.__init__(self, writer, color=color, uri=uri, refresh_duration=refresh_duration, path=path)

    def getMessage(self):
        message = int(round(JsonReader.getMessage(self)))
        if message == 100:
            return "finished!"
        else:
            return str(message).rjust(2) + u"°o"

    @staticmethod
    def getParams():
        return Program.getParams()