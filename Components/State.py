from component import Component

class State(Component):
    def __init__(self, dData):          #sComponentID, sState):
        Component.__init__(self, "STATE:%s"%(dData['componentID']), False, 0)
        self._sState = dData['state']

    def _Get_State(self):
        return self._sState
