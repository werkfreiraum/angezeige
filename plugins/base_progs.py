# -*- coding: utf-8 -*-
from programs import Program


class Counter(Program):

    def __init__(self, color=None, duration=None):
        Program.__init__(self, color=color)
        self.duration = float(self.get_params()["duration"] if duration is None else duration)

    def do(self):
        i = 0
        while True:
            signs = "%4d" % (i % 10000)
            self.write(signs)
            self.wait(self.duration)
            i += 1

    @staticmethod
    def get_params():
        params = Program.get_params()
        params['duration'] = "1"
        return params


class BlinkAll(Program):

    def __init__(self, color=None, duration=None):
        Program.__init__(self, color=color)
        self.duration = float(self.get_params()["duration"] if duration is None else duration)

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
    def get_params():
        params = Program.get_params()
        params['duration'] = "1"
        return params


class ShowSigns(Program):

    def __init__(self, color=None, signs=None):
        Program.__init__(self, color=color)
        self.signs = self.get_params()["signs"] if signs is None else signs

    def do(self):
        while True:
            self.write(self.signs)
            self.wait(10)

    @staticmethod
    def get_params():
        params = Program.get_params()
        params['signs'] = "1234"
        return params


class SlideText(Program):

    def __init__(self, color=None, text=None, slide_speed=None):
        Program.__init__(self, color=color)
        self.text = self.get_params()["text"] if text is None else unicode(text)
        self.slide_speed = float(self.get_params()["slide_speed"] if slide_speed is None else slide_speed)

    def do(self):
        while True:
            self.slide(self.text, speed=self.slide_speed)

    @staticmethod
    def get_params():
        params = Program.get_params()
        params['text'] = u"0123456789abcdefghijklmnopqrstuvwxyzäöüß?!.,-\'\""
        params['slide_speed'] = "0.4"
        return params


class FadeMe(Program):

    def __init__(self, i=None, j=None):
        Program.__init__(self, color=None)
        self.j = float(self.get_params()["j"] if j is None else j)
        self.i = float(self.get_params()["i"] if i is None else i)

    def do(self):
        j = self.j
        i = self.i
        d = False
        while True:
            self.wait(j * i)
            self.write('8888', separator="BOTH")

            self.wait((1 - j) * i)
            self.write('   ')

    @staticmethod
    def get_params():
        params = {}
        params['j'] = "1"
        params['i'] = "1"
        return params
