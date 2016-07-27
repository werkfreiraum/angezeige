from writer.base import Writer


class FileWriter(Writer):

    def __init__(self, file_name):
        self.file_name = file_name

    def enable(self):
        self.file = open(self.file_name, "wb")

    def disable(self):
        self.file.close()

    def write(self, message):
        self.file.write(message)
        self.file.flush()
