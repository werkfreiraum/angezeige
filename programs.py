# -*- coding: utf-8 -*-
import logging
import sys
from time import sleep
from core.base import *
from writer.base import WriterProxy
from threading import Thread
from conf.private import api_keys, exclude_programs


program_registry = {}


class MetaProgram(type):
    """Used for auto registering programs. No need for decorator anymore."""
    def __new__(mcs, name, bases, dict):
        new_program = type.__new__(mcs, name, bases, dict)
        if name not in program_registry and name != "Program" and name not in exclude_programs:
            program_registry[name] = new_program
        return new_program


class Program(Thread):
    checkInterval = 0.2
    running = None
    raiseException = False
    color = "white"
    prefered_signs = True
    _closing = False

    __metaclass__ = MetaProgram

    def __init__(self, color=None):
        Thread.__init__(self)
        self.daemon = True
        self._closing = False
        self._error = None
        self._last_message = None

        self.writer = WriterProxy.instance

        if "color" in self.get_params() or color is not None:
            self.color = self.get_params()["color"] if color is None else color

    def open(self):
        pass

    def run(self):
        try:
            name = self.get_program_name()
            if len(name) > 4:
                self.slide(name, speed=0.2, color="green", prefered_signs=True)
            else:
                self.write(name, color="green", prefered_signs=True)
                self.wait(1)
            self.open()
            self.do()
        except Exception as e:
            logging.exception("Exception in plugin {}".format(self.__class__))
            self.write("ERRO", color="red", prefered_signs=True)
            #self.slide("Error", speed=0.2, color="red", prefered_signs=True)
            self._error = e
            if Program.raiseException:
                raise
        sys.exit()

    def close(self):
        pass

    def error(self):
        return self._error

    def write(self, string, *args, **kwargs):
        #logging.debug(kwargs)
        if "color" not in kwargs and self.color is not None:
            kwargs["color"] = self.color
        if "prefered_signs" not in kwargs and self.prefered_signs is not None:
            kwargs["prefered_signs"] = self.prefered_signs
        #logging.debug(kwargs)
        self._last_message = get_message(string, *args, **kwargs)
        self.writer.write(self._last_message)

    def slide(self, message, speed=0.4, color=None, prefered_signs=None):
        with_spaces = ' ' * 4 + message + ' ' * 4
        for i in range(len(with_spaces) - 3):
            self.write(with_spaces[i:(i + 4)], prefered_signs=prefered_signs, color=color)
            self.wait(speed)

    # def transition(self, message, speed=0.3):
    #     for i in range(3):
    #         pass

    def wait(self, interval, show_progress=False):
        still_to_wait = interval
        while True:
            if self._closing:
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
    def get_program_name(cls, beauty = True):
        if cls.name and beauty:
            return cls.name
        else:
            return cls.__name__

    @staticmethod
    def get_promoted_programs():
        return program_registry

    @staticmethod
    def get_api_key(name):
        try:
            api_key = api_keys[name]
        except KeyError:
            raise ValueError("No api key with name: " + name)
        return api_key

    @classmethod
    def stop(cls):
        if cls.running:
            cls.running._closing = True
            cls.running.join()
            try:
                cls.running.close()
            except Exception as e:
                logging.exception("Exception while closing plugin {}".format(cls.get_promoted_programs(beauty = False)))
            cls.running = None

    @classmethod
    def start(cls, info):
        cls.stop()
        params = info["params"] if "params" in info else {}
        try:
            logging.debug("Creating program " + info['name'] + "...")
            p = cls.get_promoted_programs()[info['name']](**params)
            logging.debug("Done")
            Thread.start(p)
            cls.running = p
        except Exception as e:
            logging.exception("Exception in plugin {}".format(info['name']))
            Program._error = e
            # if Program.raiseException:
            #    raise


# import will register all Programs
from plugins import *
