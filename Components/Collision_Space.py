from component import Component
import pymunk

class Collision_Space(Component):
    def __init__(self, dData):
        Component.__init__(self, "CSPACE:%s"%(dData['componentID']), True, 0)

        self._cSpace = pymunk.Space()

        self._cSpace.gravity = (float(dData["gravity"][0]),float(dData["gravity"][1]))

    def _Add_Shape(self, cBody, cShape):
        """This is meants for adding in collision bodies into the collision space.
        @param cBody This is a pymunk Body object. It represents an Entity's body.
        @param lCShape This is a list of pymunk Shape objects. It allows multiple shapes
            to be associated with one body."""

        #print "Adding Shape into Collision Space"
        #print cBody, cShape

        #print cBody.position

        if type(cShape) is list:

            if cBody.is_static:
                #Notice the * prefix, this will unpack a list.
                self._cSpace.add(*cShape)

            else:
                #Notice the * prefix, this will unpack a list.
                self._cSpace.add(cBody, *cShape)

        else:
            if cBody.is_static:
                self._cSpace.add(cShape)

            else:
                self._cSpace.add(cBody, cShape)

    def _Add_Constraint(self, cConstraint):
        """This takes in a constraint that has already been initialed, then adds
        it into the collision space.
        @param cConstraint some instance of a constraint."""

        self._cSpace.add(cConstraint)



    def _Remove_Shape(self, cBody, cShape):
        """This is meant for removing body and shape collision objects out
        of the Collision SPace."""

        self._cSpace.remove(cBody, cShape)

    def _Get_Static_Body(self):
        """This is just for getting a static body for the collision space."""
        return self._cSpace.static_body

    def _Update(self, timeElapsed):
        """This should tell pymunk to step forward in time
        a certain amount.
        @param timeElapsed The timeElapsed is a sf.Time objecct 
            and it will be the same value each time depending on the
            update rate."""

        #This will step the physics for the Collision_Bodys through an update.
        self._cSpace.step(timeElapsed.as_seconds())
