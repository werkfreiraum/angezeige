#!/usr/bin/env python2
import time, signal, sys
import spi_dev
from programs import *

def start(writer = spi_dev.write):
    ### Different programs are defined in programs.py

    p = FirstDigitCounter(writer)
    #p = ShowTime(writer, color = "red")
    
    p.run()



def main():
    def close_sig_handler(signal, frame):
        print("\nBye!")
        sys.exit()
    
    signal.signal(signal.SIGINT, close_sig_handler)

    spi_dev.init()
    start()





if __name__ == "__main__":
    main()
