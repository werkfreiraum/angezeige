from programs import Program, promoteProgram

################################################################
# Iterates the first digit
################################################################
@promoteProgram
class Counter(Program):
    def do(self):
        i = 0
        while True:
            signs = "%4d" % (i%10000)
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
        self.duration = float(self.getParams()["duration"] if duration is None else duration)

    def do(self):
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


################################################################
# Show Signs
################################################################
@promoteProgram
class ShowSigns(Program):
    def __init__(self, writer=None, color=None, signs=None):
        Program.__init__(self, writer, color=color)
        self.signs = self.getParams()["signs"] if signs is None else signs

    def do(self):
        while True:
            self.write(self.signs)
            self.wait(10)

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['signs'] = "1234"
        return params