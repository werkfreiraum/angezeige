from proxy import Proxy


class Writer(object):

    def __init__(self):
        pass

    def write(self, message):
        pass

    def enable(self):
        pass

    def disable(self):
        pass

    def close(self):
        pass


class WriterProxy(Proxy, Writer):

    def __init__(self, items):
        Proxy.__init__(self, items)
        Writer.__init__(self)

    def write(self, message):
        for uniqueId in self.enabled_items:
            self.items[uniqueId].write(message)

    @staticmethod
    def get_imp_class(name):
        return globals()[name]


from writer.fileWriter import FileWriter
from writer.webSocketWriter import WebSocketWriter
