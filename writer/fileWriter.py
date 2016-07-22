from writer.base import Writer

class FileWriter(Writer):

    def __init__(self, file):
        self.f = open(file, "wb")

    def write(self, message):
        self.f.write(message)
        self.f.flush()

    def close(self):
        self.f.close()
