from component import Component
import pymunk


class Collision_Constraint(Component):
    """This will allow collision bodies to be attached to each other using one of several constraints.
    This component seems to only be compatible with assembler functions. Because it requires other
    CBODY components to be passed to it (which is impossible for extra components at the moment.)
    It assumes string arguments anyway for when extra components have the flexibility to receive
    component arguments.

    Important: I also am making this componet a throw away component, in that it will be removed
    from an entity as soon as the constraint is added to the collision space (it won't be needed
    thereafter.)"""
    def __init__(self, dData):
        Component.__init__(self, "CCONSTRAINT:%s"%(dData['componentID']), False, 0)

        self._constraint = None

        #body1 and body2 are assumed to be components because in the future, this component will
        #   be able to be passed components without the need of an assembler function.
        if dData["type"] == "gearJoint":
            #print "body1:", dData["body1"]._Get_Body(),         \
            #        "body2:", dData["body2"]._Get_Body(),       \
            #        "phase:", float(dData["phase"]),            \
            #        "ratio:", float(dData["ratio"])
            
            self._constraint = pymunk.GearJoint(dData["body1"]._Get_Body(),        \
                                                dData["body2"]._Get_Body(),         \
                                                float(dData["phase"]),              \
                                                float(dData["ratio"]))

            #print self._constraint

        else:
            print "!!!Invalid constraint type was chosen!!!"

    def _Get_Constraint(self):
        """The constraint needs to be retrieved so that it can be added into the collision space."""
        return self._constraint
