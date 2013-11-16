from component import Component
import sfml as sf

class Box(Component):
    def __init__(self, dData):
        Component.__init__(self, "BOX:%s"%(dData['componentID']), False, 1)
        self._box = sf.RectangleShape((int(dData['width']),int(dData['height'])))
        self._box.position = (int(dData['x']),int(dData['y']))
        self._box.fill_color = sf.Color.WHITE
        self._box.outline_color = sf.Color.RED
        self._box.outline_thickness = 3.0

    def _Set_Color(self, fillColor, outlineColor):
        self._box.fill_color = fillColor
        self._box.outline_color = outlineColor

    def _Get_Color(self):
        return self._box.fill_color

    def _Switch_Color(self):
        tmpColor = self._box.fill_color
        self._box.fill_color = self._box.outline_color
        self._box.outline_color = tmpColor

    def _Get_Box(self):
        return self._box

    def _Render(self, renderWindow):
        renderWindow.draw(self._box)
