from component import Component

class Misc(Component):
    def __init__(self, dData):
        Component.__init__(self, "MISC:%s"%(dData['componentID']), False, 0)
        self._storage = dData['storage']

    def _Set_Storage(self, variable):
        self._storage = variable

    def _Get_Storage(self):
        return self._storage
