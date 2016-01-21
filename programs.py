# -*- coding: utf-8 -*-
import logging
from time import sleep
from base import *
from spi_dev import SpiDevWriter
from private import spidev_file
from threading import Thread
import sys


program_registry = {}


class MetaProgram(type):
    """Used for auto registering programs. No need for decorator anymore."""
    def __new__(mcs, name, bases, dict):
        new_program = type.__new__(mcs, name, bases, dict)
        if name not in program_registry:
            program_registry[name] = new_program
        return new_program


class Program(Thread):
    checkInterval = 0.2
    running = None
    raiseException = False
    color = "white"
    prefered_signs = True

    __metaclass__ = MetaProgram

    def __init__(self, writer=None, color=None):
        Thread.__init__(self)
        self.daemon = True
        self._stop = False
        self._error = None
        self._last_message = None
        self._last_string = None

        self.writer = SpiDevWriter(spidev_file) if writer is None else writer

        if "color" in self.getParams() or color is not None:
            self.color = self.getParams()["color"] if color is None else color


    def run(self):
        try:
            self.do()
        except Exception as e:
            logging.exception("Exception in plugin {}".format(self.__class__))
            self._error = e
            if Program.raiseException:
                raise
        self.exit()

    def stop(self):
        self._stop = True

    def error(self):
        return self._error

    def start(self):
        #sys.stderr.write(self.get_program_name() + " started\n")
        Program.running = self
        Thread.start(self)

    def write(self, string, *args, **kwargs):
        if "color" not in kwargs and self.color is not None:
            kwargs["color"] = self.color
        if "prefered_signs" not in kwargs and self.prefered_signs is not None:
            kwargs["prefered_signs"] = self.prefered_signs
        self._last_string = string
        self._last_message = get_message(string, *args, **kwargs)
        self.writer.write(self._last_message)

    def slide(self, message, speed=0.4, color=None):
        with_spaces = ' ' * 4 + message + ' ' * 4
        for i in range(len(with_spaces) - 3):
            self.write(with_spaces[i:(i + 4)])
            self.wait(speed)

    def transition(self, message, speed=0.3):
        for i in range(3):
            pass


    def wait(self, interval, show_progress=False):
        still_to_wait = interval
        while True:
            if self._stop:
                self.exit()
            if still_to_wait <= Program.checkInterval:
                break
            else:
                sleep(Program.checkInterval)
                still_to_wait -= Program.checkInterval
                if show_progress:
                    p = int(round(float(still_to_wait) / interval * 4))
                    self._last_message = modify_separator(self._last_message, separator=("P", p), color=self.color)
                    self.writer.write(self._last_message)

        sleep(still_to_wait)

    def exit(self):
        self.writer.close()
        #sys.stderr.write(self.get_program_name() + " exit\n")
        sys.exit()

    @staticmethod
    def getParams():
        params = {}
        params['color'] = "white"
        return params

    @classmethod
    def get_program_name(cls):
        return cls.__name__

    @staticmethod
    def getPromotedPrograms():
        return program_registry


# import will register all Programs
from plugins import *
