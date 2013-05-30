class PriorityQueue(object):
    """This is meant for storing Entities for the Entity_Manager,
    Entity and Entity_List classes. The primary function of this
    priority queue is to list entities in a specific draw order."""
    def __init__(self, lEntities=[]):

        #This will hold the items of the Queue
        #   with respect to the priority Values from
        #   the dictionary of priorityValues.
        #The first item of the list should be the
        #   first item that is drawn. And a priority of
        #   zero means the corresponding entities will be drawn first.
        self._lEntities = []

        for i in xrange(len(lEntities)-1,-1,-1):

            self._Add_Entity(lEntities.pop(i))

    def _Add_Entity(self, entity):
        """This is for adding Entities to the PriorityQueue.
        This allows the given Entity to be drawn to the screen."""

        #This searches through the list for the entity.
        for i in xrange(len(self._lEntities)+1):

            #This checks to see if the i is within the bounds of the list
            #This is because of the len(self._lEntities)+1 given to xrange.
            if (i != len(self._lEntities)):

                #Check to see if we've found the entity.
                if (self._lEntities[i]._Get_Name() == entity._Get_Name()    \
                    and self._lEntities[i]._Get_Type() == entity._Get_Type()):

                    print "%s already exists within the PriorityQueue!"%(entity._Get_Type()+"-"+entity._Get_Name())
                    return None

        if len(self._lEntities) == 0:
            self._lEntities.append(entity)

        else:

            #This will search through the Entities for one that has the same priority or
            #   more than what the Entity being added in has.
            for i in xrange(len(self._lEntities)+1):
                
                #This checks to see if we made it through the list of Entities without finding
                #   one with a priority equal or greater than the one being added.
                #   If this is true, we can just add the entity to the end of the list.
                if (i == len(self._lEntities)):

                    self._lEntities.append(entity)
                    
                elif self._lEntities[i]._Get_Draw_Priority() \
                    >= entity._Get_Draw_Priority():

                    #Insert the Entity into the list at the current location (which will move the item we checked
                    #   against, back a space.)
                    self._lEntities.insert(i, entity)

                

            
    def _Remove_Entity(self, sEntityName, sEntityType):
        """This is meant for taking an Entity out of the
        Priority Queue.
        @param sEntityName This name identifies the entity that
            will be removed.
        @param sEntityType This type identifies the entity that
            will be removed.
        @post The dPriorityValues and lEntities will both be missing
            an element."""

        #This searches through the list for the entity.
        for i in xrange(len(self._lEntities)+1):

            #This checks to see if the i is within the bounds of the list
            #This is because of the len(self._lEntities)+1 given to xrange.
            if (i != len(self._lEntities)):

                #Check to see if we've found the entity.
                if (self._lEntities[i]._Get_Name() == sEntityName       \
                    and self._lEntities[i]._Get_Type() == sEntityType):

                    del self._lEntities[i]                   

                break

            #This extra addition to the list
            #   is only reached when the entity wasn't
            #   found, so we will print a message.
            else:
                #pass
                print "%s:%s wasn't able to be removed from the priority queue."%(sEntityType, sEntityName)


    def __getitem__(self, indx):
        """Since the Entities are inserted with respect to their priority into the list. It
        is possible to just iterate through the list of Entities.
        @param indx THis is the indx within the list the entity is retrieved from.
        @return The entity that is at the indx given."""

        return self._lEntities[indx]



    def __len__(self):
        """This will simply return the length of the
        list of entities within the Priority Queue."""
        
        return len(self._lEntities)

    def _Clear(self):
        """This will remove all of the Entities and
        priority values within the PriorityQueue."""

        del self._lEntities[:]
        






                
        
