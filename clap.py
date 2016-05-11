#!/usr/bin/env python2
import pyaudio
import sys
import thread
from time import sleep
from array import array
from threading import Thread

chunk = 1024 * 10
threshold = 32760  # almost 2^16/2

from private import audio as audio_settings

_stream = None
_p = None

detected = False
_close = False
_thread = None


def open():
    global _stream, _p
    _p = pyaudio.PyAudio()

    audio_settings['format'] = pyaudio.paInt16
    audio_settings['input'] = True
    audio_settings['output'] = False
    audio_settings['frames_per_buffer'] = chunk

    _stream = _p.open(**audio_settings)


def _detect(ret_func=None):
    global detected
    while True:
        data = _stream.read(chunk)
        as_ints = array('h', data)
        max_value = max(as_ints)
        if _close:
            exit()
        if max_value > threshold:
            if ret_func is not None:
                ret_func()
            detected = True


def start_detection(ret_func=None):
    global _thread
    _thread = Thread(target=_detect, args=(ret_func, ))
    _thread.start()


def close():
    global _close
    _close = True
    _thread.join()
    _stream.stop_stream()
    _stream.close()
    _p.terminate()
