import json
import urllib2
import re
import logging
from contextlib import closing

from private import api_keys
from programs import Program


# TODO:
#   - need some description on display for minute contdown
#   - need better display values for NaN, inf, and zero (asterisk!)
#   - fair use? how many connections allowed by api?
#   - hardcoded constants ---> params
#   - find nice way to store secrets

URL = "http://www.wienerlinien.at/ogd_realtime/monitor?rbl={}&sender={}"
api_key = api_keys['wienerlinien_ogd_realtime']

# TODO I guess this needs refactoring, dict was used for other project that way
STATION_IDS = {
    'K': '4210',    # U2 Rathaus, Richtung Karlsplatz
    'A': '4205',    # U2 Rathaus, Richtung Aspern

    # Westbahnhof:
    'U3-H':   4921,
    'U3-R':   4920,
    'U6-H':   4619,
    'U6-R':   4610,
    '5':      370,
    '6-H':    464,  # Mariahilfer Guertel ist viell. naher
    '6-R':    483,
    '9':      484,
    '52':     36,   # Gerstnerstrasse ist naeher
    '58':     1531,
    'N64-H':  5772,
    'N64-R':  5658,

    # Gerstnerstrasse/Westbhf.
    '52-H':    1548,
    '52-R':    1549,

    # Mariahilfer Guertel
    '6-H':     482,
    '6-R':     481,
}

JSON_PATH = 'data.monitors[0].lines[0].departures.departure[0].departureTime.countdown'
CYCLE_PERIOD_S = 2
FAILURE_RETRY_PERIOD_S = 10



def _get_val_by_path(dct, path):
    """Returns element from dictionary ``dct`` along path ``path``."""
    for i, p in re.findall(r'(\d+)|(\w+)', path):
        dct = dct[p or int(i)]
    return dct


################################################################
# Show when next bim comes
################################################################
class NextBim(Program):
    def do(self):
        while True:
            for cmd, station_id in STATION_IDS.iteritems():
                logging.debug('Retrieving countdown for station={}'.format(
                    station_id))
                api_uri = URL.format(station_id, api_key)
                try:
                    # need contextlib because no Python 3... :(
                    with closing(urllib2.urlopen(api_uri)) as nextbims_json:
                        nextbim = json.load(nextbims_json)
                except urllib2.URLError:
                    logging.exception("Failed to retrieve nextbim data.")
                    self.write('')
                else:
                    countdown = _get_val_by_path(nextbim, JSON_PATH)
                    logging.info('Countdown={} for station={}'.format(
                        countdown, station_id))
                    self.write(str(countdown))
                self.wait(CYCLE_PERIOD_S)
