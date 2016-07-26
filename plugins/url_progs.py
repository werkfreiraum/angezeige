# -*- coding: utf-8 -*-
import json
import logging
from programs import Program
import urllib2
import re
from contextlib import closing


class UrlReader(Program):
    timeout = 1

    def __init__(self, color=None, uri=None, refresh_duration=None):
        Program.__init__(self, color=color)
        self.uri = self.get_params()["uri"] if uri is None else uri
        self.refresh_duration = float(self.get_params()["refresh_duration"]
                                      if refresh_duration is None else refresh_duration)

    @staticmethod
    def get_params():
        params = Program.get_params()
        params['uri'] = "http://spartan.ac.brocku.ca/~tmulligan/3p82inv_hand.html"
        params['refresh_duration'] = "20"
        return params

    def do(self):
        while True:
            message = self.getMessage()
            if len(message) > 4:
                self.slide(message, speed=0.3)
            else:
                self.write(message)
            self.wait(self.refresh_duration, show_progress=True)

    def getMessage(self):
        return self.readUri().rstrip()

    def readUri(self):
        # try:
            # need contextlib because no Python 3... :(
        with closing(urllib2.urlopen(self.uri, timeout=self.timeout)) as f:
            return f.read()
        # except urllib2.URLError as e:
        #    logging.exception("Failed to retrieve data from url.")
        #    raise e

    def setUri(self, uri):
        self.uri = uri


class JsonReader(UrlReader):

    def __init__(self, color=None, uri=None, refresh_duration=None, path=None):
        UrlReader.__init__(self, color=color, uri=uri, refresh_duration=refresh_duration)
        self.path = self.get_params()["path"] if path is None else path

    @staticmethod
    def get_val_by_path(dct, path):
        """Returns element from dictionary ``dct`` along path ``path``."""
        for i, p in re.findall(r'(\d+)|(\w+)', path):
            dct = dct[p or int(i)]
        return dct

    @staticmethod
    def get_params():
        params = UrlReader.get_params()
        params['path'] = "a.b"
        return params

    def getMessage(self):
        return self.readJsonPathContent()

    def readJsonPathContent(self, dct=None, path=None):
        if path is None:
            path = self.path
        if dct is None:
            dct = self.readUri()
        return JsonReader.get_val_by_path(json.loads(dct), path)


class ViennaTemp(JsonReader):
    name = "tEMP"

    @staticmethod
    def get_params():
        params = {}
        return params

    def __init__(self):
        refresh_duration = 180
        path = "main.temp"
        JsonReader.__init__(self, uri="pospone", refresh_duration=refresh_duration, path=path)

    def open(self):
        api_key = self.get_api_key('OpenWeatherMap')
        uri = "http://api.openweathermap.org/data/2.5/weather?id=2761369&units=metric&APPID=" + api_key
        self.setUri(uri)

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
                temperature = temperature * -1

            temperature_str = str(temperature)
            if temperature >= 0 and temperature < 10:
                temperature_str = " " + temperature_str

            self.color = color

            self.write(unicode(temperature_str) + u"°C", prefered_signs=False)
            self.wait(self.refresh_duration, show_progress=True)
