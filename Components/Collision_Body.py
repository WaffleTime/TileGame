from component import Component
import pymunk

class Collision_Body(Component):
    def __init__(self, dData):
        Component.__init__(self, "CBODY:%s"%(dData['componentID']), False, 0)

        mass = None
        inertia = None
        
        if dData["MomentType"] == "static":
            pass

        elif dData["MomentType"] == "circle":
            mass = int(dData["mass"])
            radius = int(dData["radius"])
            inertia = pymunk.moment_for_circle(mass, 0, radius)

        elif dData["MomentType"] == "box":
            mass = int(dData["mass"])
            width = int(dData["width"])
            height = int(dData["height"])

            inertia = pymunk.moment_for_box(mass, width, height)
            
        self._cBody = pymunk.Body(mass, inertia)

    def _Get_Body(self):
        """This is for returning the collision body."""
        return self._cBody
