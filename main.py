#!/usr/bin/env python2
import sys
import signal
import logging
from programs import Program
from chooser import choose
import clap

LOG_FORMAT = '%(asctime)s - %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='DEBUG', filename="angezeige.log")


def cleanup_exit(*kwargs):
    print("\nBye!")
    if Program.running:
        Program.running.stop()
        Program.running.join()
    clap.close()
    sys.exit()


def main():
    signal.signal(signal.SIGINT, cleanup_exit)

    clap.open()
    clap.start_detection()

    choose()
    cleanup_exit()


if __name__ == "__main__":
    main()
