#!/usr/bin/env python2
import signal
import logging
from programs import Program
from chooser import UrwidChooser
from switches.base import *
from writer.base import *

from conf.private import writer, switches, switch_programs_file

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")


def main():

    def cleanup_exit(*args, **kwargs):
        print("\nBye!")
        Program.stop();
        s.disable()
        w.disable()
        exit()

    signal.signal(signal.SIGINT, cleanup_exit)

    w = WriterProxy(items=writer)
    s = SwitchProxy(items=switches, switch_programs_file=switch_programs_file)

    w.enable()
    s.enable()

    Program.start(s.next())

    c = UrwidChooser()
    c.start()

    cleanup_exit()


if __name__ == "__main__":
    main()
