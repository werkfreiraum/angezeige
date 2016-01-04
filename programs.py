from time import gmtime, strftime, sleep
from base import *

class Program(object):
    promotedPrograms = {}
    writer = None
    color = None
    def __init__(self, writer, color = None):
        print(" - Program: " + self.get_program_name())
        self.writer = writer
        self.color = color

    def run(self):
        pass

    def write(self, *args, **kwargs):
        if "color" not in kwargs and self.color is not None:
            kwargs["color"] = self.color
        self.writer(get_message(*args, **kwargs))

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
            sleep(1)
            i += 1
