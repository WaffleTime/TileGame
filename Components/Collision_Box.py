from Collision_Shape import Collision_Shape
import pymunk
import config

class Collision_Box(Collision_Shape):
    def __init__(self, dData):

        cBody = None

        width = int(dData["width"])
        height = int(dData["height"])

        if dData["collisionType"] != "static":

            mass = int(dData["mass"])
            
            inertia = pymunk.moment_for_box(mass, width, height)

            cBody = pymunk.Body(mass, inertia)

        else:
            
            cBody = dData["staticBody"]

        #This assumes that the dData["yOffset"] is with respect to Pysfml's coordante plane.
        cBody.position = (dData["xOffset"], config.WINDOW_HEIGHT-dData["yOffset"]-int(dData["height"]))

        cBox = pymunk.Poly(cBody,                                         \
                           [ (0,height),    \
                             (width,height),     \
                             (width,0),    \
                             (0,0) ],\
                           (0, 0),                                        \
                           False)

        """cBox = pymunk.Poly(cBody,                                         \
                           [ (-width/2,height/2),    \
                             (width/2,height/2),     \
                             (width/2,-height/2),    \
                             (-width/2, -height/2) ],\
                           (0, 0),                                        \
                           False)"""

        #This will load the Collision_Shape up with the Shape and data that it needs.
        Collision_Shape.__init__(self,      \
                                 cBox,      \
                                 cBody,     \
                                 {"componentID":dData["componentID"],     \
                                  "dependentComponentName":dData["dependentComponentName"]})

