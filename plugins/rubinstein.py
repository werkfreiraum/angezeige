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
        #message = int(round(JsonReader.getMessage(self)))
        message = 100
        if message == 100:
            return "FiniShEd"
        else:
            return str(message).ljust(2) + u"°o"




################################################################
# Show when printer rubinstein ready
################################################################
# class RubinsteinProgress(Program):
#     def do(self):
#         while True:
#             for key, param_paths in PARAMTERS.iteritems():
#                 for param_path in param_paths:
#                     api_uri = "{}{}?apikey={}".format(URL, key, api_key)
#                     try:
#                         # need contextlib because no Python 3... :(
#                         with closing(urllib2.urlopen(api_uri)) as params_json:
#                             params = json.load(params_json)
#                     except urllib2.URLError:
#                         logging.exception("Failed to retrieve rubinstein"
#                                           "data.")
#                         self.write('')
#                     else:
#                         param = int(round(_get_val_by_path(params, param_path)))
#                         self.write(str(param))
#                     self.wait(CYCLE_PERIOD_S)
