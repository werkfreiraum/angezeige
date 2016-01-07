# -*- coding: utf-8 -*-
from programs import Program, promoteProgram
import urllib
import json

################################################################
# Shows text from URL
################################################################
@promoteProgram
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





@promoteProgram
class ViennaTemp(Program):
    @staticmethod
    def getParams():
        params = {}
        return params

    def do(self):
        api_key = ''
        url = "http://api.openweathermap.org/data/2.5/weather?id=2761369&units=metric&APPID=" + api_key
        if api_key == '':
            raise Exception("No openweathermap API key provided!")

        while True:
            f = urllib.urlopen(url)
            j = json.loads(f.read())
            f.close()
            
            temp = int(round(float(j["main"]["temp"])))

            if temp > 0:
                color = "orange"
            else:
                color = "blue"

            if temp >= 0 and temp < 10:
                temp = " " + str(temp)

            self.write(unicode(temp) + u"°C", color=color)
            self.wait(180)