from component import Component


class Collision_Shape(Component):
    def __init__(self, cShape, cBody, dData):
        Component.__init__(self, "CSHAPE:%s"%(dData['componentID']), False, 0)

        self._sDependent_Comp_Name = dData["dependentComponentName"]

        self._cShape = cShape

        self._cBody = cBody

    def _Get_Shape(self):
        """This is for retrieving the collision shape. It's
        important that all Collision Shape components have a method
        with this exact name. It's used by Entity_PQueue to get the shapes
        within Entities and load them into the collision space with their body (_Add_Entity() is
        the method I speak of.)"""

        return self._cShape

    def _Get_Body(self):
        """This is for retrieving the body of the collision shape.
        It's also necessary within the Entity_PQueue._Add_Entity() method.
        @return A Pymunk Body object that is to be connected to the collision shape
            within the collision space."""

        return self._cBody

    def _Get_Dependent_Comp_Name(self):
        """This is for retrieving the name of the component
        that this collision shape affects."""

        return self._sDependent_Comp_Name
