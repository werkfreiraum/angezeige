import logging
from programs import Program
from url_progs import JsonReader


# TODO:
#   - need some description on display for minute contdown
#   - need better display values for NaN, inf, and zero (asterisk!)
#   - fair use? how many connections allowed by api?
#   - hardcoded constants ---> params
#   - find nice way to store secrets


# TODO I guess this needs refactoring, dict was used for other project that way
# STATION_IDS = {
#     'K': '4210',    # U2 Rathaus, Richtung Karlsplatz
#     'A': '4205',    # U2 Rathaus, Richtung Aspern

#     # Westbahnhof:
#     'U3-H':   4921,
#     'U3-R':   4920,
#     'U6-H':   4619,
#     'U6-R':   4610,
#     '5':      370,
#     '6-H':    464,  # Mariahilfer Guertel ist viell. naher
#     '6-R':    483,
#     '9':      484,
#     '52':     36,   # Gerstnerstrasse ist naeher
#     '58':     1531,
#     'N64-H':  5772,
#     'N64-R':  5658,

#     # Gerstnerstrasse/Westbhf.
#     '52-H':    1548,
#     '52-R':    1549,

#     # Mariahilfer Guertel
#     '6-H':     482,
#     '6-R':     481,
# }

#FAILURE_RETRY_PERIOD_S = 10



class NextBim(JsonReader):
    name = 'NEXT'

    baseUrl = "http://www.wienerlinien.at/ogd_realtime/monitor"

    def __init__(self, steig=None, color=None):
        refresh_duration = 10
        path = 'data.monitors[0].lines[0].departures.departure[0].departureTime.countdown'
        self.prefered_signs = False
        self.steig = steig
        JsonReader.__init__(self, color=color, uri="posponed", refresh_duration=refresh_duration, path=path)

    def open(self):
        self.setUri("{}?rbl={}&sender={}".format(self.baseUrl, self.steig, self.get_api_key('wienerlinien_ogd_realtime')))

    def getMessage(self):
        minutes = int(JsonReader.getMessage(self))
        return "??" + str(minutes).rjust(2)

    @staticmethod
    def get_params():
        params = {}
        params['steig'] = "4619"
        params['color'] = "white"
        return params


class NextU6Wbhf(NextBim):
    name = 'U6'

    def __init__(self):
        NextBim.__init__(self, steig=4619, color="brown")

    def getMessage(self):
        minutes = int(JsonReader.getMessage(self))
        return "U6" + str(minutes).rjust(2)

    @staticmethod
    def get_params():
        return {}


class Next52Gerst(NextBim):
    name = '52'

    def __init__(self):
        NextBim.__init__(self, steig=1548, color="white")

    def getMessage(self):
        minutes = int(JsonReader.getMessage(self))
        return "52" + str(minutes).rjust(2)

    @staticmethod
    def get_params():
        return {}


class U3(NextBim):
    name = 'U3'

    def __init__(self):
        NextBim.__init__(self, steig=4291, color="red")

    def getMessage(self):
        #minutes = int(JsonReader.getMessage(self))
        # return "U3" + str(minutes).rjust(2)
        return "U300"

    @staticmethod
    def get_params():
        return {}

