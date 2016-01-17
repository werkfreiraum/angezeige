# -*- coding: utf-8 -*-
import json
import urllib
import logging
from programs import Program
from private import api_keys
################################################################
# Shows text from URL
################################################################
class UrlReader(Program):
    def __init__(self, writer=None, color=None, url=None, duration=None):
        Program.__init__(self, writer, color=color)
        self.url = self.getParams()["url"] if url is None else url
        self.duration = float(self.getParams()["duration"] if duration is None else duration)

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['url'] = "http://angezeige.abteil.org/nr.html"
        params['duration'] = "2"
        return params

    def do(self):
        separator = ["INNER", "NONE"]
        while True:
            f = urllib.urlopen(self.url)
            self.write(f.read(4))
            f.close()
            self.wait(self.duration)


class ViennaTemp(Program):
    @staticmethod
    def getParams():
        params = {}
        return params

    def do(self):
        try:
            api_key = api_keys["OpenWeatherMap"]
        except KeyError:
            logging.exception("Failed to start OpenWeatherMap.")
            raise ValueError("No openweathermap API key provided!")

        url = "http://api.openweathermap.org/data/2.5/weather?id=2761369&units=metric&APPID=" + api_key

        while True:
            f = urllib.urlopen(url)
            j = json.loads(f.read())
            f.close()

            temp = int(round(float(j["main"]["temp"])))

            if temp <= 0:
                color = "blue"
            elif temp > 0 and temp < 15:
                color = "orange"
            elif temp >= 15:
                color = "red"

            if temp >= 0 and temp < 10:
                temp = " " + str(temp)

            if temp < -9:
                temp = temp*-1

            self.write(unicode(temp) + u"°C", color=color)
            self.wait(180)
