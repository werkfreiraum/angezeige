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
        params['uri'] = "http://angezeige.abteil.org/nr.html"
        params['refresh_duration'] = "2"
        return params

    def do(self):
        try:
            # need contextlib because no Python 3... :(
            with closing(urllib2.urlopen(api_uri)) as params_json:
                params = json.load(params_json)
        except urllib2.URLError:
            logging.exception("Failed to retrieve rubinstein"
                              "data.")
            self.write('')
        else:
            param = int(round(_get_val_by_path(params, param_path)))
            self.write(str(param))
        self.wait(CYCLE_PERIOD_S)

        separator = ["INNER", "NONE"]
        while True:
            f = urllib.urlopen(self.uri)
            self.write(f.read(4))
            f.close()
            self.wait(self.refresh_duration)

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
        params['path'] = "http://angezeige.abteil.org/nr.html"
        return params

    def do(self):
        separator = ["INNER", "NONE"]
        while True:
            f = urllib.urlopen(self.url)
            self.write(f.read(4))
            f.close()
            self.wait(self.duration)

    def readJsonPathContent(self):
        dct = json.loads(self.readUri())
        return _get_val_by_path(dct, self.path)



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

            self.write(unicode(temperature_str) + u"°C", color=color)
            self.wait(self.refresh_duration)
