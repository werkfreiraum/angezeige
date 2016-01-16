import json
import urllib2
import re
import logging
from contextlib import closing

from private import api_keys
from programs import Program
from programs import promoteProgram


URL = "http://rubinstein.local/api/"
PARAMTERS = {
    'job': [
        'progress.completion',
        #'job.estimatedPrintTime',  # TODO should convert to hh:mm
    ]
}
CYCLE_PERIOD_S = 10
api_key = api_keys['rubinstein']


def _get_val_by_path(dct, path):
    """Returns element from dictionary ``dct`` along path ``path``."""
    for i, p in re.findall(r'(\d+)|(\w+)', path):
        dct = dct[p or int(i)]
    return dct


################################################################
# Show when printer rubinstein ready
################################################################
@promoteProgram
class Rubinstein(Program):
    def do(self):
        while True:
            for key, param_paths in PARAMTERS.iteritems():
                for param_path in param_paths:
                    api_uri = "{}{}?apikey={}".format(URL, key, api_key)
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
