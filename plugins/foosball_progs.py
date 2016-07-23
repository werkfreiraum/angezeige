# -*- coding: utf-8 -*-
import json
import logging
from programs import Program
from url_progs import UrlReader, JsonReader

URI_FOOSBALL = "http://foosball.local:5000"


class SimpleFoosball(UrlReader):

    def __init__(self, uri=None):
        UrlReader.__init__(self, uri=uri, refresh_duration=0)

    @staticmethod
    def get_params():
        params = {}
        params['uri'] = URI_FOOSBALL
        return params


# class ColorFoosball(UrlReader):

#     def __init__(self, uri=None):
#         UrlReader.__init__(self, uri=uri, refresh_duration=0)

#     @staticmethod
#     def get_params():
#         params = {}
#         params['uri'] = URI_FOOSBALL + "/color"
#         return params

#     def do(self):
#         while True:

#             d_info = json.loads(self.readUri())
#             JsonReader.get_val_by_path(j_dct, "color")

#              = self.getMessage()


#             return JsonReader.get_val_by_path(j_dct, path)
#                 self.write(message)
#             self.wait(self.refresh_duration, show_progress=False)
