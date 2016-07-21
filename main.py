#!/usr/bin/env python2
import sys
import signal
import logging
import json
from programs import Program
from chooser import choose
from switch import *
from switch import *

from conf.private import switches

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")


def cleanup_exit(**kwargs):
    print("\nBye!")
    if Program.running:
        Program.running.stop()
        Program.running.join()
    switches.close()
    sys.exit()


def main():
    global switches
    switches = Switches(switches)

    with open('./conf/switch_programs.json') as data_file:
        switch_programs = json.load(data_file)

    switches.start_detection()

    signal.signal(signal.SIGINT, cleanup_exit)

    choose(use_switch=switches, use_switch_programs=switch_programs)
    cleanup_exit(switch=switches)


if __name__ == "__main__":
    main()
