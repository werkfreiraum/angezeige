from programs import Program, promoteProgram

################################################################
# Iterates the first digit
################################################################
@promoteProgram
class Counter(Program):
    def __init__(self, writer=None, color=None, duration=None):
        Program.__init__(self, writer, color=color)
        self.duration = float(self.getParams()["duration"] if duration is None else duration)

    def do(self):
        i = 0
        while True:
            signs = "%4d" % (i%10000)
            self.write(signs)
            self.wait(self.duration)
            i += 1

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['duration'] = "1"
        return params

################################################################
# Blink all leds
################################################################
@promoteProgram
class BlinkAll(Program):
    def __init__(self, writer=None, color=None, duration=None):
        Program.__init__(self, writer, color=color)
        self.duration = float(self.getParams()["duration"] if duration is None else duration)

    def do(self):
        show = True
        message_show = {
            "string": "8888",
            "separator": "BOTH"
        }
        message_hide = {
            "string": "",
            "separator": "NONE"
        }
        while True:
            if show:
                self.write(**message_show)
            else:
                self.write(**message_hide)
            show = not show
            self.wait(self.duration)

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


################################################################
# Show Signs
################################################################
@promoteProgram
class ScrollText(Program):
    def __init__(self, writer=None, color=None, text=None, duration=None):
        Program.__init__(self, writer, color=color)
        self.text = self.getParams()["text"] if text is None else text
        self.duration = float(self.getParams()["duration"] if duration is None else duration)

    def do(self):
        i = 0
        while True:
            self.write(('    ' + self.text + '    ')[i:(i+4)])
            self.wait(self.duration)
            i += 1
            if i >= len(self.text) + 4:
                i = 0

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['text'] = "Ich bin ScrollbAr"
        params['duration'] = "0.5"
        return params

################################################################
# Fade
################################################################
@promoteProgram
class FadeMe(Program):
    def __init__(self, writer=None, i=None, j=None):
        Program.__init__(self, writer, color=None)
        self.j = float(self.getParams()["j"] if j is None else j)
        self.i = float(self.getParams()["i"] if i is None else i)    
    def do(self):
        j = self.j
        i = self.i
        d = False
        while True:

            # if d:
            #     j-=1;
            # else:
            #     j+=1;

            # if j >= 100:
            #     d = True
            # if j <= 0:
            #     d = False

            self.wait(j*i)
            self.write('8888',separator="BOTH")

            self.wait((1-j)*i)
            self.write('   ')
    @staticmethod
    def getParams():
        params = {}
        params['j'] = "1"
        params['i'] = "1"
        return params