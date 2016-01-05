#!/usr/bin/env python2
import time, signal, sys
from spi_dev import SpiDevWriter
from programs import Program
from chooser import choose

def cleanup_exit(*kwargs):
    print("\nBye!")
    if Program.running:
        Program.running.stop()
        Program.running.join()
    sys.exit()

def main():
    signal.signal(signal.SIGINT, cleanup_exit)
    choose()
    cleanup_exit()

if __name__ == "__main__":
    main()
