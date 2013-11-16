from component import Component


class Dictionary(Component):
    """This is for containing Chunks."""
    def __init__(self, dData):
        Component.__init__(self, "DICT:%s"%(dData['componentID']), False, 0)
        #This can also hold entities
        self._dComponents = {}

    def _Add(self, itemName, item):
        self._dComponents[itemName] = item

    def _Remove(self, itemName):
        del self._dComponents[itemName]

    def __getitem__(self, key):
        return self._dComponents.get(key, None)

    def __setitem__(self, key, value):
        self._dComponents[key] = value

    def values(self):
        return self._dComponents.values()

    def __str__(self):
        return str(self._dComponents)

    def _Clear(self):
        del self._lComponents

    def _Get(self, itemName):
        return self._dComponents.get(itemName, None)
