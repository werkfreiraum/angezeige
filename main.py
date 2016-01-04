#!/usr/bin/env python2
import time, signal, sys
from spi_dev import SpiDevWriter
from programs import *
from chooser import choose

#spidev_file = "/tmp/spidev0.0"
spidev_file = "/dev/spidev0.0"
writer = None

def start(writer = None, program = None):
    ### Different programs are defined in programs.py
    if program is None:
        ### CHOOSE ONE
        #p = FirstDigitCounter(writer)
        p = ShowTime(writer, color = "red")
        #p = BlinkAll(writer, color = "blue")
    else:
        p = Program.getPromotedPrograms()[program[0]](writer, **program[1])
    p.run()


def cleanup_exit(*kwargs):
    print("\nBye!")
    if writer:
        writer.close()
    sys.exit()

def main():
    global writer
    signal.signal(signal.SIGINT, cleanup_exit)
    writer = SpiDevWriter(spidev_file)
    start(writer = writer, program = choose())
    cleanup_exit()

if __name__ == "__main__":
    main()
