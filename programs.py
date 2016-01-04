from time import gmtime, strftime, sleep
from base import *


class Program(object):
    promotedPrograms = {}
    def __init__(self, writer, color = None):
        print(" - Program: " + self.get_program_name())
        self.writer = writer
        self.color = self.getParams["color"] if color is None else color

    def run(self):
        pass

    def write(self, *args, **kwargs):
        if "color" not in kwargs and self.color is not None:
            kwargs["color"] = self.color
        self.writer.write(get_message(*args, **kwargs))

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
        i = 0
        separator = ["BOTH", "NONE"]
        while True:
            signs = strftime("%H%M", gmtime())
            self.write(signs, separator = separator[i%len(separator)])
            sleep(1)
            i += 1


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
            sleep(1)
            i += 1


################################################################
# Blink all leds
################################################################
@promoteProgram
class BlinkAll(Program):
    def __init__(self, writer, color=None, duration=None):
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
            sleep(self.duration)
            i += 1

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['duration'] = "1"
        return params


@promoteProgram
class ShowSigns(Program):
    def __init__(self, writer, color=None, signs=None):
        Program.__init__(self, writer, color=color)
        self.signs = self.getParams["signs"] if signs is None else signs

    def run(self):
        while True:
            self.write(self.signs)
            sleep(10)

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['signs'] = "1234"
        return params