# -*- coding: utf-8 -*-
import json
import urllib
import logging
from programs import Program
from private import api_keys
import urllib2
import re
import logging
from contextlib import closing

################################################################
# Shows text from URL
################################################################
class UrlReader(Program):
    def __init__(self, writer=None, color=None, uri=None, refresh_duration=None):
        Program.__init__(self, writer, color=color)
        self.uri = self.getParams()["uri"] if uri is None else uri
        self.refresh_duration = float(self.getParams()["refresh_duration"] if refresh_duration is None else refresh_duration)

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['uri'] = "http://spartan.ac.brocku.ca/~tmulligan/3p82inv_hand.html"
        params['refresh_duration'] = "20"
        return params

    def do(self):
        while True:
            message = self.getMessage()
            if len(message) > 4:
                self.slide(message, slide_speed=0.3)
            else:
                self.write(message)
            self.wait(self.refresh_duration, show_progress = True)

    def getMessage(self):
        return self.readUri().rstrip()

    def readUri(self):
        try:
            # need contextlib because no Python 3... :(
            with closing(urllib2.urlopen(self.uri)) as f:
                return f.read()
        except urllib2.URLError:
            logging.exception("Failed to retrieve rubinstein"
                              "data.")
            self.write('Error')
            raise 


def _get_val_by_path(dct, path):
    """Returns element from dictionary ``dct`` along path ``path``."""
    for i, p in re.findall(r'(\d+)|(\w+)', path):
        dct = dct[p or int(i)]
    return dct


class JsonReader(UrlReader):
    def __init__(self, writer=None, color=None, uri=None, refresh_duration=None, path=None):
        UrlReader.__init__(self, writer, color=color, uri=uri, refresh_duration=refresh_duration)
        self.path = self.getParams()["path"] if path is None else path

    @staticmethod
    def getParams():
        params = UrlReader.getParams()
        params['path'] = "a.b"
        return params

    def getMessage(self):
        return self.readJsonPathContent()

    def readJsonPathContent(self, path = None):
        if path is None:
            path = self.path
        dct = json.loads(self.readUri())
        return _get_val_by_path(dct, path)



class ViennaTemp(JsonReader):
    @staticmethod
    def getParams():
        params = {}
        return params

    def __init__(self, writer=None):
        try:
            api_key = api_keys["OpenWeatherMap"]
        except KeyError:
            logging.exception("Failed to start OpenWeatherMap.")
            raise ValueError("No openweathermap API key provided!")

        uri = "http://api.openweathermap.org/data/2.5/weather?id=2761369&units=metric&APPID=" + api_key
        refresh_duration = 180
        path = "main.temp"
        JsonReader.__init__(self, writer, uri=uri, refresh_duration=refresh_duration, path=path)

    def do(self):
        while True:
            temperature = int(round(float(self.readJsonPathContent())))

            if temperature <= 0:
                color = "blue"
            elif temperature > 0 and temperature < 15:
                color = "orange"
            elif temperature >= 15:
                color = "red"

            if temperature < -9:
                temperature = temperature*-1

            temperature_str = str(temperature)
            if temperature >= 0 and temperature < 10:
                temperature_str = " " + temperature_str

            self.color = color

            self.write(unicode(temperature_str) + u"°C")
            self.wait(self.refresh_duration, show_progress = True)
