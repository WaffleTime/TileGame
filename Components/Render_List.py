from component import Component

class Render_List(Component):
    """This is meant for containing Chunk Entities."""
    def __init__(self, dData):
        Component.__init__(self, "RLIST:%s"%(dData['componentID']), False, 2)
        #This can also hold entities.
        self._lComponents = []

    def _Add(self, item):
        self._lComponents.append(item)

    def _Clear(self):
        for i in xrange(len(self._lComponents)-1,-1,-1):
            del self._lComponents[i]

    def _Remove(self, indx):
        del self._lComponents[indx]

    def _Pop(self, indx):
        return self._lComponents.pop(indx)

    def __getitem__(self, indx):
        return self._lComponents[indx]

    def __len__(self):
        return len(self._lComponents)

    def _Render(self, renderWindow):

        for i in xrange(len(self._lComponents)):

            self._lComponents[i]._Get_Component("MESH:0")._Render(renderWindow)

