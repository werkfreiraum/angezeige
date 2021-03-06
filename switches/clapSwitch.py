from array import array
from threading import Thread
import sys
from switches.base import Switch

class ClapSwitch(Switch):

    def __init__(self, ret_func=None, threshold=32760, chunk=1024 * 10):
        Switch.__init__(self, ret_func=None)
        self.chunk = chunk
        self.threshold = threshold

    def enable(self):
        self.closing = False

        import pyaudio
        from conf.private import audio as audio_settings

        self.pas = pyaudio.PyAudio()

        audio_settings['format'] = pyaudio.paInt16
        audio_settings['input'] = True
        audio_settings['output'] = False
        audio_settings['frames_per_buffer'] = self.chunk

        self.stream = self.pas.open(**audio_settings)

        self.thread = Thread(name="ClapSwitch Detector", target=self._detect)
        self.thread.start()

    def disable(self):
        if self.thread.is_alive():
            self.closing = True
            self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.pas.terminate()

    def _detect(self):
        while True:
            data = self.stream.read(self.chunk)
            as_ints = array('h', data)
            max_value = max(as_ints)
            if self.closing:
                sys.exit()
            if max_value > self.threshold:
                self._detected()
