from component import Component
import pymunk
import config

class Collision_Body(Component):
    """This is meant for static/nonstatic cBodies with multiple or a single shape that have an
    associated sprite that should move with respect to this body. This component is actually
    supported by the main.py's xml parser. CollisionShapes are collected into a list of dictionaries."""
    def __init__(self, dData):
        Component.__init__(self, "CBODY:%s"%(dData['componentID']), False, 0)

        height = None

        if dData["static"] == "NO":
            mass = None
            inertia = None
        
            if dData["MomentType"] == "circle":
                mass = int(dData["mass"])
                radius = int(dData["radius"])
                height = radius*2
                inertia = pymunk.moment_for_circle(mass, 0, radius)

            elif dData["MomentType"] == "box":
                mass = int(dData["mass"])
                width = int(dData["width"])
                height = int(dData["height"])

                inertia = pymunk.moment_for_box(mass, width, height)

            self._cBody = pymunk.Body(mass, inertia)

        elif dData["static"] == "UPRIGHT":
            height = int(dData["height"])
            self._cBody = pymunk.Body(int(dData["mass"]), pymunk.inf)
            
        else:
            height = int(dData["height"])
            self._cBody = pymunk.Body(pymunk.inf, pymunk.inf)

        

        self._cBody.position = (int(dData["xOffset"]), config.WINDOW_HEIGHT-int(dData["yOffset"])-height)

        self._sDependent_Component_ID = dData["dependentComponentID"]

        self._cShapes = {}

        #The cShapes element is a list and it contains dictionaries of attributes for a single shape.
        for dAttribs in dData["CollisionShape"]:
            if dAttribs["type"] == "circle":
                cCircle = pymunk.Circle(self._cBody, int(dAttribs["radius"]), (int(dAttribs["xBodyOffset"]), int(dAttribs["yBodyOffset"])))

                cCircle.friction = float(dAttribs["friction"])

                self._cShapes[dAttribs["name"]] = cCircle

            elif dAttribs["type"] == "box":
                cBox = pymunk.Poly(self._cBody,                                       \
                         [(-int(dAttribs["width"])/2,int(dAttribs["height"])/2),                               \
                         (int(dAttribs["width"])/2,int(dAttribs["height"])/2),                \
                         (int(dAttribs["width"])/2,-int(dAttribs["height"])/2),                                 \
                         (-int(dAttribs["width"])/2,-int(dAttribs["height"])/2)],                                                \
                         (int(dAttribs["xBodyOffset"]), int(dAttribs["yBodyOffset"])),    \
                         False)

                cBox.friction = float(dAttribs["friction"])

                self._cShapes[dAttribs["name"]] = cBox


    def _Get_Dependent_Component_ID(self):
        """This is for retrieving the name of the component
        that this collision body affects."""

        return self._sDependent_Component_ID

    def _Get_Shape(self, sName):
        """For retrieving a specific shape within the body."""
        return self._cShapes[sName]

    def _Get_Shapes(self):
        """Returns a list of shapes so that they can be added to the Collision_Space."""
        return self._cShapes.values()


    def _Get_Body(self):
        """This is for returning the collision body."""
        return self._cBody

