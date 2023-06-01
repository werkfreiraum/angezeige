from writer.base import Writer
from spidev import SpiDev

class SpiDevWriter(Writer):
    def __init__(self, bus = 0, device = 0, max_speed_hz = 250000):
        self.bus = 0
        self.device = 0
        self.max_speed_hz = max_speed_hz

        self.spi = SpiDev()

    def enable(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = self.max_speed_hz 

    def disable(self):
        self.spi.close()

    def write(self, message):
        self.spi.writebytes(message)
