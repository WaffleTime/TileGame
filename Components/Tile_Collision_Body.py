from component import Component
import pymunk
import config

class Tile_Collision_Body(Component):
    """This is a custom class for the collidable tiles.
    It exists so that hard coded values are allowed. Which
    reduces string to int casting."""
    def __init__(self, dData):
        Component.__init__(self, "CTILEBODY:%s"%(dData['componentID']), False, 0)

        self._sDependent_Component_ID = dData["dependentComponentID"]

        self._cBody = dData["staticBody"]

        self._cBody.position = dData["xOffset"], config.WINDOW_HEIGHT-dData["yOffset"]-dData["height"]

        cBox = pymunk.Poly(self._cBody,                                 \
                 [(0,dData["height"]),                                  \
                 (dData["width"],dData["height"]),                      \
                 (dData["width"],0),                                    \
                 (0,0)],                                                \
                 (0,0),                                                 \
                 False)
        cBox.friction = dData["friction"]

        self._cShape = cBox

    def _Get_Dependent_Component_ID(self):
        """This is for retrieving the name of the component
        that this collision body affects."""

        return self._sDependent_Component_ID

    def _Get_Shape(self):
        """Gets the collision shape so that it can be added to the Collision_Space."""
        return self._cShape
        
    def _Get_Body(self):
        """This is for returning the collision body."""
        return self._cBody
