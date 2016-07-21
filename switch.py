#!/usr/bin/env python2
import sys
import thread
from time import sleep
from array import array
from threading import Thread



class Switch(object):
    detected = False
    forward = None

    def __init__(self, ret_func=None):
        self.ret_func = ret_func

    def set_forward(self, forward):
        self.forward = forward

    def start_detection(self):
        pass

    def close(self):
        pass

    def _detected(self):
        self.detected = True
        if self.ret_func:
            self.ret_func(self)
        if forward:
            forward._detected()


class Switches(object):
    detected = False
    switches = {}

    def __init__(self, switches):
        for uniqueId, info in switches.iteritems():
            switchType = info["type"]
            params = info["params"] if "params" in prog else {} 
            self.add_switch(uniqueId, switchType, params = params)


    def add_switch(self, uniqueId, switchType, params = {}, active = True):
        switch = globals()[type](**params)
        switch.set_forward(self)
        self.switches[uniqueId] = switch

    def start_detection(self):
        for s in self.switches:
            if self.switches[s]['active']:
                self.switches[s].start_detection()

    def stop_detection(self):
        for s in self.switches:
            if self.switches[s]['active']:
                s.stop_detection()

    def close(self):
        for s in self.switches:
            self.switches[s].close()

    def _detected(self):
        self.detected = True


class SimpleSwitch(Switch):
    pin = 4
    bounce_time = 400
    ret_func = None

    def __init__(self, ret_func=None, pin=4, bounce_time=400, edge = "falling"):
        Switch.__init__(self, ret_func=None)
        self.pin = pin
        self.bounce_time = 400
        self.ret_func = None

        global GPIO
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def close(self):
        pass

    def start_detection(self):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._detected, bouncetime=self.bounce_time)

    def stop_detection(self):
        GPIO.remove_event_detect(self.pin)


class ClapSwitch(Switch):
    thread = None
    stream = None
    pas = None
    closing = False

    def __init__(self, ret_func=None, threshold=32760, chunk=1024 * 10):
        Switch.__init__(self, ret_func=None)
        self.chunk = chunk
        self.threshold = threshold

        import pyaudio
        from conf.private import audio as audio_settings

        self.pas = pyaudio.PyAudio()

        audio_settings['format'] = pyaudio.paInt16
        audio_settings['input'] = True
        audio_settings['output'] = False
        audio_settings['frames_per_buffer'] = chunk

        self.stream = self.pas.open(**audio_settings)

    def start_detection(self):
        self.closing = False
        self.thread = Thread(target=self._detect, args=(ret_func, ))
        self.thread.start()

    def _detect(self):
        while True:
            data = self.stream.read(self.chunk)
            as_ints = array('h', data)
            max_value = max(as_ints)
            if self.closing:
                exit()
            if max_value > self.threshold:
                self._detected()

    def stop_detection(self):
        if self.thread.is_alive():
            self.closing = True
            self.thread.join()

    def close(self):
        self.stop_detection()

        self.stream.stop_stream()
        self.stream.close()
        self.pas.terminate()
