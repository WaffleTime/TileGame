import components
from PriorityQueue import PriorityQueue as PQ

from Entity import Entity

class Entity_PQueue(Entity):
    """Like the name says, this will store Entities. And it will update/render those entities accordingly."""
    def __init__(self, sName, sType, iDrawPriority, dAttribs):

        Entity.__init__(self, sName, sType, iDrawPriority, {})

        #This takes all of the entities out of the dComponents
        dEntities = dAttribs.pop("entity", {})

        #"These are the entities that are being loaded into the Entity_PQueue"
        #print dEntities

        #This orders the entities so that the ones with the highes t draw
        #   priority will be first in the list (highest priority is 0.)
        self._pqEntities = PQ()

        #This is Pymunk's Space() class basically. But it's in a component.
        #   It will contain the collidable object for Entities.
        Entity._Add_Component( self, components.Collision_Space( {"componentID":"EntityPool",     \
                                                                 "gravity":dAttribs["gravity"].split(",")} ) )

        #This will insert the entities into the PriorityQueue through the proper method.
        for entity in dEntities.values():

            self._Add_Entity(entity)

        

    def _Add_Entity(self, entity):
        """This will add entities into our dictionary of lists of entities.
        And it will also add the Entity to the PriorityQueue so that it can be drawn.
        @param entity This should be an actual instance of the Entity class. So it
            holds components and that's about it.
        @param iPriority This is the draw priority for the Entity that it being
            added. Zero is the highest draw priority (gets drawn first,) -1 means
            the Entity doesn't need added to the PriorityQueue."""


        print "%s:%sEntity is being added into the PriorityQueue"%(entity._Get_Type(), entity._Get_Name())


        self._pqEntities._Add_Entity(entity)

        if entity._Get_All_Components("CSHAPE") != []:
            #The ENtity must first be flagged so that its render updates
            #   take care of the continuously moving collision shapes.
            entity._Set_Collidable(True)

            for component in entity._Get_All_Components("CSHAPE"):

                #Each CShape within this entity will be added to the EntityPool.
                self._Get_Component("CSPACE:EntityPool")._Add_Shape(component._Get_Body(), component._Get_Shape())

        else:
                entity._Set_Collidable(False)

    def _Remove_Entity(self, sEntityTypeName, sEntityName):
        """When an entity expires it will be removed with this."""

        #Entities that aren't within the priority queue will be ignored.
        self._pqDrawableEntities._Remove_Entity(sEntityTypeName, sEntityName)

    def _Get_Entity(self, sEntityTypeName, sEntityName):
        """This is for retrieving entities from the dictionary."""

        for i in xrange(len(self._pqEntities)):

            if self._pqEntities[i]._Get_Name() == sEntityName  \
               and self._pqEntities[i]._Get_Type() == sEntityTypeName:

                return self._pqEntities[i]

        return None

    def _Update(self, timeElapsed):
        """This will be where we update all of the contained entities. (This happens once per game update!)"""

        Entity._Update(self, timeElapsed)
        
        for indx in xrange(len(self._pqEntities)):
            #This will check to see if the current Entity has signaled to be removed.
            if self._pqEntities[indx]._Is_Expired():
                #So we let the entity do its cleaning up, then we remove it from the Entity_List entirely.
                self._pqEntities[indx]._On_Expire()
                self._Remove_Entity(self._pqEntities[indx]._Get_Name())
                #We won't need to update a removed entity!
                break

            #Now since that this entity hasn't been removed, we'll update it.
            self._pqEntities[indx]._Update(timeElapsed)

    def _Render(self, renderWindow, windowView):
        """Here we render the contained entities onto the screen. (This happens once per program loop!)"""

        Entity._Render(self, renderWindow, windowView)

        for indx in xrange(len(self._pqEntities)):
            self._pqEntities[indx]._Render(renderWindow, windowView)
