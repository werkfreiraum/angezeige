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

    __metaclass__ = MetaProgram

    def __init__(self, writer=None, color=None):
        Thread.__init__(self)
        self.daemon = True
        self._stop = False
        self._error = None
        self.color = None

        self.writer = SpiDevWriter(spidev_file) if writer is None else writer

        if "color" in self.getParams():
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

    def write(self, *args, **kwargs):
        if "color" not in kwargs and self.color is not None:
            kwargs["color"] = self.color
        self.writer.write(get_message(*args, **kwargs))

    def wait(self, interval):
        while True:
            if self._stop:
                self.exit()
            if interval <= Program.checkInterval:
                break
            else:
                sleep(Program.checkInterval)
                interval -= Program.checkInterval

        sleep(interval)

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
