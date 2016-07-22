#!/usr/bin/env python2
import sys
import signal
import logging
from programs import Program
from chooser import choose
from switches.base import *

from conf.private import switches, switch_programs_file

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")


def main():

    def cleanup_exit(*args, **kwargs):
        print("\nBye!")
        if Program.running:
            Program.running.stop()
            Program.running.join()
        switch.close()
        sys.exit()

    signal.signal(signal.SIGINT, cleanup_exit)

    switch = Switches(switches=switches, switch_programs_file=switch_programs_file)
    switch.start_detection()

    choose()

    cleanup_exit()


if __name__ == "__main__":
    main()
