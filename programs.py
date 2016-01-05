from time import gmtime, strftime, sleep
from base import *
from spi_dev import SpiDevWriter
from settings import spidev_file
from threading import Thread
import sys



class Program(Thread):
    checkInterval = 0.05
    promotedPrograms = {}
    running = None

    def __init__(self, writer = None, color = None):
        Thread.__init__(self)
        self.daemon = True
        self._stop = False

        self.writer = SpiDevWriter(spidev_file) if writer is None else writer

        self.color = self.getParams["color"] if color is None else color

    def run(self):
        pass

    def stop(self):
        self._stop = True

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
        return Program.promotedPrograms


def promoteProgram(programClass):
    Program.promotedPrograms[programClass.__name__] = programClass
    return programClass


################################################################
# Shows current time
################################################################
@promoteProgram
class ShowTime(Program):
    def run(self):
        separator = ["INNER", "NONE"]
        while True:
            signs = strftime("%H%M", gmtime())
            sec = int(strftime("%S", gmtime()))
            self.write(signs, separator = separator[sec%len(separator)])
            self.wait(0.1)


################################################################
# Iterates the first digit
################################################################
@promoteProgram
class FirstDigitCounter(Program):
    def run(self):
        i = 0
        while True:
            signs = "%1d" % (i%10)
            self.write(signs)
            self.wait(1)
            i += 1


################################################################
# Blink all leds
################################################################
@promoteProgram
class BlinkAll(Program):
    def __init__(self, writer=None, color=None, duration=None):
        Program.__init__(self, writer, color=color)
        self.duration = float(self.getParams["duration"] if duration is None else duration)

    def run(self):
        i = 0
        messages = [
            {
                "string": "8888",
                "separator": "BOTH"
            }, {
                "string": "",
                "separator": "NONE"
            }
        ]

        while True:
            self.write(**messages[i%len(messages)])
            self.wait(self.duration)
            i += 1

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['duration'] = "1"
        return params


@promoteProgram
class ShowSigns(Program):
    def __init__(self, writer=None, color=None, signs=None):
        Program.__init__(self, writer, color=color)
        self.signs = self.getParams["signs"] if signs is None else signs

    def run(self):
        while True:
            self.write(self.signs)
            self.wait(10)

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['signs'] = "1234"
        return params