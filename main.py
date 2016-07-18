#!/usr/bin/env python2
import sys
import signal
import logging
from programs import Program
from chooser import choose
from switch import *

externSwitch = None
switch = None

if externSwitch == "clap":
    switch = ClapSwitch()

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")


def cleanup_exit(*kwargs):
    print("\nBye!")
    if Program.running:
        Program.running.stop()
        Program.running.join()
    if switch:
        switch.close()
    sys.exit()


def main():
    signal.signal(signal.SIGINT, cleanup_exit)

    switch_programs = None
    if switch:
        with open('./switch_programs.json') as data_file:
            switch_programs = json.load(data_file)
        switch.open()
        switch.start_detection()

    choose(use_switch=switch, use_switch_programs=switch_programs)
    cleanup_exit()


if __name__ == "__main__":
    main()
