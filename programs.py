# -*- coding: utf-8 -*-
import logging
import sys
from time import sleep
from core.base import *
from writer.base import WriterProxy
from threading import Thread


program_registry = {}


class MetaProgram(type):
    """Used for auto registering programs. No need for decorator anymore."""
    def __new__(mcs, name, bases, dict):
        new_program = type.__new__(mcs, name, bases, dict)
        if name not in program_registry and name != "Program":
            program_registry[name] = new_program
        return new_program


class Program(Thread):
    checkInterval = 0.2
    running = None
    raiseException = False
    color = "white"
    prefered_signs = True
    closing = False

    __metaclass__ = MetaProgram

    def __init__(self, color=None):
        Thread.__init__(self)
        self.daemon = True
        self.closing = False
        self._error = None
        self._last_message = None
        #self._last_string = None

        self.writer = WriterProxy.instance

        if "color" in self.get_params() or color is not None:
            self.color = self.get_params()["color"] if color is None else color

    def run(self):
        try:
            self.do()
        except Exception as e:
            logging.exception("Exception in plugin {}".format(self.__class__))
            self._error = e
            if Program.raiseException:
                raise
        sys.exit()

    def stop(self):
        self.closing = True

    def error(self):
        return self._error

    def start(self):
        Program.running = self
        Thread.start(self)

    def write(self, string, *args, **kwargs):
        if "color" not in kwargs and self.color is not None:
            kwargs["color"] = self.color
        if "prefered_signs" not in kwargs and self.prefered_signs is not None:
            kwargs["prefered_signs"] = self.prefered_signs
        #self._last_string = string
        self._last_message = get_message(string, *args, **kwargs)
        self.writer.write(self._last_message)

    def slide(self, message, speed=0.4, color=None, prefered_signs=None):
        with_spaces = ' ' * 4 + message + ' ' * 4
        for i in range(len(with_spaces) - 3):
            self.write(with_spaces[i:(i + 4)], prefered_signs=prefered_signs)
            self.wait(speed)

    def transition(self, message, speed=0.3):
        for i in range(3):
            pass

    def wait(self, interval, show_progress=False):
        still_to_wait = interval
        while True:
            if self.closing:
                sys.exit()
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
        

    @staticmethod
    def get_params():
        params = {}
        params['color'] = "white"
        return params

    @classmethod
    def get_program_name(cls):
        return cls.__name__

    @staticmethod
    def get_promoted_programs():
        return program_registry

    @classmethod
    def start_program(cls, info):
        if cls.running:
            cls.running.stop()
            cls.running.join()

        params = info["params"] if "params" in info else {}

        p = cls.get_promoted_programs()[info['name']](**params)
        p.start()


# import will register all Programs
from plugins import *
