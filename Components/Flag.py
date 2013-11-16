from component import Component

class Flag(Component):
    """This is a piece of logic for Buttons and will tell the button's _box object
    to oscillate its color scheme whenever collisions occur with the mouse and the button."""
    def __init__(self, dData):
        Component.__init__(self, "FLAG:%s"%(dData['componentID']), False, 0)
        self._flag = dData['flag']

    def _Set_Flag(self, isActive):
        self._flag = isActive

    def _Get_Flag(self):
        return self._flag
