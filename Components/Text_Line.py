from component import Component
import sfml as sf

class Text_Line(Component):
    def __init__(self, dData):  # sComponentID, xPos, yPos, width, height, text, font):
        Component.__init__(self, "TEXTLINE:%s"%(dData['componentID']), False, 1)
        self._text = sf.Text(dData['text'], dData['font'])
        self._text.color = sf.Color.BLACK
        self._text.style = sf.Text.UNDERLINED
        self._text.x = int(dData['x']) + int(dData['width']) / 2.0 - self._text.global_bounds.width / 2.0
        self._text.y = int(dData['y']) + int(dData['height']) / 2.0 - self._text.global_bounds.height / 2.0

    def _Render(self, renderWindow):
        
        renderWindow.draw(self._text)
