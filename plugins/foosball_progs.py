# -*- coding: utf-8 -*-
import json
import logging
from programs import Program
from url_progs import UrlReader, JsonReader

URI_FOOSBALL = "http://foosball.local:5000"


class WebServerFoosball(UrlReader):

    def __init__(self, uri=None):
        UrlReader.__init__(self, uri=uri, refresh_duration=0)

    @staticmethod
    def get_params():
        params = {}
        params['uri'] = URI_FOOSBALL
        return params


class TestSimpleFoosball(Program):

    def __init__(self, uri=None):
        Program.__init__(self)

    def do(self):
        while True:
            self.write("1234", color=["blue", "white", "green", "orange"])
            self.wait(1)

    @staticmethod
    def get_params():
        params = {}
        params['uri'] = URI_FOOSBALL
        return params


class DirectFoosball(Program):

    pin_red = 14
    pin_blue = 15

    pin_reset = 18

    bounce_time = 2000

    score = [0, 0]

    def __init__(self):
        Program.__init__(self)
        global GPIO
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_blue, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_reset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.pin_red, GPIO.FALLING, callback=self.goal, bouncetime=self.bounce_time)
        GPIO.add_event_detect(self.pin_blue, GPIO.FALLING, callback=self.goal, bouncetime=self.bounce_time)

        GPIO.add_event_detect(self.pin_reset, GPIO.FALLING, callback=self.resetGoals, bouncetime=self.bounce_time)

    def goal(self, channel):
        logging.debug("GOAL" + str(channel))
        self.update = True
        if channel == self.pin_red:
            self.score[0] += 1
        if channel == self.pin_blue:
            self.score[1] += 1

    def do(self):
        while True:
            self.write('{:2}{:2}'.format(*self.score), color=['red','red','blue','blue'], seperator_color=['white']*4)
            self.wait(0.1)

    def resetGoals(channel):
        self.score = [0, 0]

    @staticmethod
    def get_params():
        return {}
