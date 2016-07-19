#!/usr/bin/env python2
import sys
import thread
from time import sleep
from array import array
from threading import Thread


class Switch(object):
    thread = None
    detected = False
    closing = False

    def open(self):
        pass

    def _detect(self, ret_func=None):
        pass

    def start_detection(self, ret_func=None):
        self.thread = Thread(target=self._detect, args=(ret_func, ))
        self.thread.start()

    def close(self):
        self.closing = True
        self.thread.join()


class SimpleSwitch(Switch):
    pin = 4
    default = 1

    def open(self):
        global GPIO
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def _detect(self, ret_func=None):
        while True:
            a = GPIO.input(self.pin)
            if self.closing:
                exit()
            if a != self.default:
                if ret_func is not None:
                    ret_func()
                self.detected = True
            sleep(0.02)


class ClapSwitch(Switch):
    chunk = 1024 * 10
    threshold = 32760  # almost 2^16/2
    stream = None
    p = None

    def open(self):
        import pyaudio
        from conf.private import audio as audio_settings

        self.p = pyaudio.PyAudio()

        audio_settings['format'] = pyaudio.paInt16
        audio_settings['input'] = True
        audio_settings['output'] = False
        audio_settings['frames_per_buffer'] = self.chunk

        self.stream = self.p.open(**audio_settings)

    def _detect(self, ret_func=None):
        while True:
            data = self.stream.read(self.chunk)
            as_ints = array('h', data)
            max_value = max(as_ints)
            if self.closing:
                exit()
            if max_value > self.threshold:
                if ret_func is not None:
                    ret_func()
                self.detected = True

    def close(self,):
        Switch.close(self)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
