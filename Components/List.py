from component import Component

class List(Component):
    """This is for containing Components as well as Entities."""
    def __init__(self, dData):
        Component.__init__(self, "LIST:%s"%(dData['componentID']), False, 0)
        #This can also hold entities.
        self._lComponents = []

    def _Add(self, item):
        self._lComponents.append(item)

    def _Clear(self):
        for key in self._lComponents.keys():
            self._lComponents.pop(key)

    def _Remove(self, indx):
        del self._lComponents[indx]

    def _Pop(self, indx):
        return self._lComponents.pop(indx)

    def __getitem__(self, indx):
        return self._lComponents[indx]

    def __setitem__(self, indx, item):
        self._lComponents[indx] = item

    def __str__(self):
        return str(self._lComponents)

    def __len__(self):
        return len(self._lComponents)
