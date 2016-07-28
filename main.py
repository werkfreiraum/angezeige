#!/usr/bin/env python2
import signal
import logging
from programs import Program
from switches.base import SwitchProxy
from writer.base import WriterProxy
from manager.base import ManagerProxy

from conf.private import writer, switches, manager, switch_programs_file

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")


def main():

    def cleanup_exit(*args, **kwargs):
        print("\nBye!")
        Program.stop()
        s.disable()
        w.disable()
        exit()

    signal.signal(signal.SIGINT, cleanup_exit)

    w = WriterProxy(items=writer)
    s = SwitchProxy(items=switches, switch_programs_file=switch_programs_file)
    m = ManagerProxy(items=manager)

    # Start first program in circle
    Program.start(s.next())

    w.enable()
    s.enable()

    # is blocking if urwid enabled
    # urwid has to be run in the main thread
    m.enable()
    if not m.is_urwid_enabled():
        signal.pause()

    cleanup_exit()


if __name__ == "__main__":
    main()
