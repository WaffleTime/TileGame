from component import Component

class Position(Component):
    def __init__(self, dData):
        Component.__init__(self, "POS:%s"%(dData['componentID']), False, 0)
        self._position = [int(dData['positionX']), int(dData['positionY'])]


    def _Get_Position(self):
        return self._position

    def _Get_X(self):
        return self._position[0]

    def _Get_Y(self):
        return self._position[1]

    def _Set_Position(self, position):
        self._position = position

    def _Add_To_X(self, number):
        self._position[0] += number

    def _Add_To_Y(self, number):
        self._position[1] += number
