#!/usr/bin/env python2
import sys
import signal
import logging
import json
from programs import Program
from chooser import choose
from switch import *

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")

def cleanup_exit(**kwargs):
    print("\nBye!")
    if Program.running:
        Program.running.stop()
        Program.running.join()
    if "switch" in kwargs:
        kwargs["switch"].close()
    sys.exit()


def main():
    externSwitch = None
    externSwitch = "clap" 

    if externSwitch == "clap":
        switch = ClapSwitch()
    elif externSwitch == "simple":
        switch = SimpleSwitch()

    signal.signal(signal.SIGINT, cleanup_exit)

    switch_programs = None
    if switch:
        with open('./conf/switch_programs.json') as data_file:
            switch_programs = json.load(data_file)
        switch.open()
        switch.start_detection()

    choose(use_switch=switch, use_switch_programs=switch_programs)
    cleanup_exit(switch = switch)


if __name__ == "__main__":
    main()
