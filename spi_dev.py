class SpiDevWriter:
    def __init__(self, spidev_file):
        self.f = open(spidev_file, "wb")

    def write(self, message):
        self.f.write(message)
        self.f.flush()

    def close(self):
        self.f.close()