#!/usr/bin/env python2
import time, signal, sys
import spi_dev
from programs import *
from chooser import choose

def start(writer = spi_dev.write, program = None):
    ### Different programs are defined in programs.py
    if program is None:
        ### CHOOSE ONE
        #p = FirstDigitCounter(writer)
        p = ShowTime(writer, color = "red")
        #p = BlinkAll(writer, color = "blue")
    else:
        p = Program.getPromotedPrograms()[program](writer)

    p.run()

def main():
    def close_sig_handler(signal, frame):
        print("\nBye!")
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    spi_dev.init()

    p = choose()
    start(program = p)

if __name__ == "__main__":
    main()
