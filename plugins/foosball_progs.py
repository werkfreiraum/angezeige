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


class DirectFoosball(Program):

    pins = [14, 15]
    team_colors = ['red', 'blue']

    update = {'type': 'reset'}
    pin_reset = 18
    bounce_time = 2000

    score = [0, 0]

    def __init__(self):
        Program.__init__(self)
        global GPIO
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_reset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.pins[0], GPIO.FALLING, callback=self.goal, bouncetime=self.bounce_time)
        GPIO.add_event_detect(self.pins[1], GPIO.FALLING, callback=self.goal, bouncetime=self.bounce_time)

        GPIO.add_event_detect(self.pin_reset, GPIO.FALLING, callback=self.resetGoals, bouncetime=self.bounce_time)

    def goal(self, channel):
        logging.debug("GOAL" + str(channel))
        self.update = {
            'type': 'goal',
            'team': channel
        }

    def do(self):
        while True:
            if self.update is not None:
                if self.update['type'] == 'goal':
                    team = self.pins.index(self.update['team'])
                    self.score[team] += 1
                    for i in range(3):
                        self.write("GOAL", color=self.team_colors[team], prefered_signs=False)
                        self.wait(0.3)
                        self.write("")
                        self.wait(0.3)
                elif self.update['type'] == 'reset':
                    self.score = [0, 0]
                    self.slide('RESET')
                    self.wait(0.5)
                self.update = None

                self.write('{:2}{:2}'.format(*self.score), color=['red'] * 2 + ['blue'] * 2)
            self.wait(0.1)

    def resetGoals(channel):
        self.update = {
            'type': 'reset'
        }

    @staticmethod
    def get_params():
        return {}
