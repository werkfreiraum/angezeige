#!/usr/bin/env python2
import signal
import logging
from programs import Program
from chooser import choose
from switches.base import *
from writer.base import *

from conf.private import writer, switches, switch_programs_file

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")


def main():

    def cleanup_exit(*args, **kwargs):
        print("\nBye!")
        if Program.running:
            Program.running.stop()
            Program.running.join()
        s.close()
        w.close()
        exit()

    signal.signal(signal.SIGINT, cleanup_exit)

    w = WriterProxy(writer=writer)

    s = SwitchProxy(switches=switches, switch_programs_file=switch_programs_file)
    s.start_detection()
    s._detected()

    choose()

    cleanup_exit()


if __name__ == "__main__":
    main()
