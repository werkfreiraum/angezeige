class Writer(object):

    def __init__(self):
        pass

    def write(self, message):
        pass

    def close(self):
        pass


class WriterProxy(Writer):
    writer = {}
    instance = None

    def __init__(self, writer):
        for uniqueId, info in writer.iteritems():
            writerType = info["type"]
            params = info["params"] if "params" in info else {}
            self.add(uniqueId, writerType, params=params)

        WriterProxy.instance = self

    def add(self, uniqueId, writerType, params={}):
        writer = globals()[writerType](**params)
        self.writer[uniqueId] = writer

    def close(self):
        for s in self.writer:
            self.writer[s].close()

    def write(self, message):
        for s in self.writer:
            self.writer[s].write(message)


from writer.fileWriter import FileWriter
from writer.webSocketWriter import WebSocketWriter