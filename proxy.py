class Proxy(object):

    def __init__(self, items):
        self.items = {}
        self.enabled_items = []
        for uniqueId, info in items.iteritems():
            itemType = info["type"]
            params = info["params"] if "params" in info else {}
            enabled = info["enabled"] if "enabled" in info else True
            self.add_item(uniqueId, itemType, enabled, params=params)

        type(self).instance = self

    def add_item(self, uniqueId, itemType, enabled, params={}):
        item = self.get_imp_class(itemType)(**params)
        self.items[uniqueId] = item
        if enabled:
            self.enabled_items.append(uniqueId)

    def enable(self, uniqueId=None):
        if uniqueId:
            if uniqueId not in self.enabled_items:
                self.items[uniqueId].start_detection()
                self.enabled_items.append(uniqueId)
        else:
            for uniqueId in self.enabled_items:
                self.items[uniqueId].enable()

    def is_enabled(self, uniqueId):
        return (uniqueId in self.enabled_items)

    def disable(self, uniqueId=None):
        if uniqueId in self.enabled_items:
            self.switches[uniqueId].stop_detection()
            self.enabled_items.remove(uniqueId)
        else:
            for uniqueId in self.enabled_items:
                self.items[uniqueId].disable()
            self.enabled_items = []
