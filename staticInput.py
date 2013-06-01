import config

def Check_Collision(targetX, targetY, targetWidth, targetHeight, x, y, width=0, height=0):
    """This is used to check to see if the target is colliding with the non-target."""

    #Are we doing a box collision check?
    if width != 0:
        
        #print "Ax:%d, Aw:%d, Bx:%d, Bw:%d" % (x, width, targetX, targetWidth)
        if (x > targetX and x < targetX + targetWidth) or (x + width > targetX and x + width < targetX + targetWidth):
            
            #print "Ay:%d, Ah:%d, By:%d, Bh:%d" % (y, height, targetY, targetHeight)
            if (y > targetY and y < targetY + targetHeight) or (y + height > targetY and y + height < targetY + targetHeight):
                return True

    else:
        #We're just collision checking a point against the target rectangle.
        if (x > targetX and x < targetX + targetWidth):
            if (y > targetY and y < targetY + targetHeight):
                return True

    return False

class TreeNode(object):
    """This is for a quad tree that handles collision detection of squares. (Crucial note)
    Remember that when a hotspot is comfirmed to be collided with, it is popped out of the place it was at (that seemed like it'd be better than adding another variable to the hotspot items.)
    But it will be added back into the QuadTree once it is no longer being collided with (it's being stored in Input_Manager.lSelectedHotspots.)"""
    def __init__(self, x, y, width, height):
        #Each item will look like so: (x, y, width, height, sPressedInputType, (selectedSystemFuncName, lSelectedEntities), (deselectedSystemFuncName, lDeselectedEntities), (pressedSystemFuncName, lPressedEntities), (releasedSystemFuncName, lReleasedEntities))
        self._items = []

        #This is so we can tell where this node is in relation to the mouse.
        self._dimensions = (x,y,width,height)

        #These are the four subnodes that will be created if the self._items container gets too full.
        #[[topLeft,topRight],[bottomLeft,bottomRight]]
        self._subnodes = [[None,None],[None,None]]

    def _Reset_Node(self):
        """This will be for when we want to add some new hotspots into the QuadTree and have no more use for the previous ones."""
        #I guess we just need to overwrite these variables (which tells the garbage collector to delete the previous contents.)
        self._items = []
        self._subnodes = [[None,None],[None,None]]

    def _Add_Item(self, item):
        """This expects to take in a tuple of data and will basically just insert it into the spot in the quad tree that it belongs in."""
        #Check to see if this node has any data that may be stored within it (if not, the data is within a subnode.)
        if self._subnodes[0][0] != None:
            for yIndx in xrange(2):
                for xIndx in xrange(2):
                    #This checks collision between the item and the current square within this node.
                    if Check_Collision(self._dimensions[0]+(self._dimensions[2]/2*xIndx), \
                                             self._dimensions[1]+(self._dimensions[3]/2*yIndx), \
                                             self._dimensions[2]/2, \
                                             self._dimensions[3]/2, \
                                             item[0],         \
                                             item[1],         \
                                             item[2],         \
                                             item[3]):
                        #This item may be added to a number of different subnodes!
                        self._subnodes[yIndx][xIndx]._Add_Item(item)
                        #print self._subnodes[yIndx][xIndx], "SUBNODE BEING ADDED TOOOOOO!"

        else:
            #This is a leaf-node, so we may want to add to it (or add subnodes that will be new leaf-nodes)
            
            #Whether we are moving the items into subnodes or not, we'll have to add the item to the list of items.
            #The False means that this item wasn't already activated by a collision with the mouse.
            #This variable allows us to be able to only activate the onSelected function once
            #(we execute the function if there's a collision and if this variable is False. If the variable in the last condition is True we do nothing.
            #And once there is no collision anymore we will switch that variable to False once more.)
    
            self._items.append(item)

            #print self._items, "This is in the elseeeeee"

            #Has this node become full?
            if len(self._items) >= 3:

                #Instantiate the subnodes
                for yIndx in xrange(2):
                    for xIndx in xrange(2):
                        self._subnodes[yIndx][xIndx] = TreeNode(self._dimensions[0]+(self._dimensions[2]/2*xIndx),  \
                                                                self._dimensions[1]+(self._dimensions[3]/2*yIndx),  \
                                                                self._dimensions[2]/2,  \
                                                                self._dimensions[3]/2)

                #print "These are the items that are being added into subnodes!", "\n", self._items

                #Iterate through the list of items to see which subnode they should go into.
                for indx in xrange(len(self._items)):
                    #This will be what allows us to make the below call to check collisions with respect to the four different squares within the screen.
                    for yIndx in xrange(2):
                        for xIndx in xrange(2):
                            #This checks collision between the item and the current square within this node.
                            if Check_Collision(self._dimensions[0]+(self._dimensions[2]/2*xIndx), \
                                                     self._dimensions[1]+(self._dimensions[3]/2*yIndx), \
                                                     self._dimensions[2]/2, \
                                                     self._dimensions[3]/2, \
                                                     self._items[indx][0], \
                                                     self._items[indx][1], \
                                                     self._items[indx][2], \
                                                     self._items[indx][3]):
                                #A polygon may be added to a number of different subnodes (as long as they collide in one way or another.)
                                self._subnodes[yIndx][xIndx]._Add_Item(self._items[indx])

                                #print self._subnodes[yIndx][xIndx]._items, "herder"
                            else:
                                pass
                                """print "No collisions here...", self._dimensions[0]+(self._dimensions[2]/2*xIndx), \
                                                     self._dimensions[1]+(self._dimensions[3]/2*yIndx), \
                                                     self._dimensions[2]/2, \
                                                     self._dimensions[3]/2, \
                                                     self._items[indx][0], \
                                                     self._items[indx][1], \
                                                     self._items[indx][2], \
                                                     self._items[indx][3]"""
                                #print "\n"

                #print self._subnodes[0][0]._items, self._subnodes[0][1]._items, self._subnodes[1][0]._items, self._subnodes[1][1]._items
                #print self._items

                
                #This is for removing the items from this node, without signaling for them to be cleaned up by the garbage collector
                #   (the items are all stored in this node's subnode now.)
                for indx in xrange(len(self._items)-1,-1,-1):
                    self._items.pop(indx)

                

            else:
                pass
                #print "Not going to move into the subnodes..."

    def _Get_Items(self):
        return self._items

    def _Get_Selected_Hotspot_Data(self, mousePos):
        """This will essentially look through the quad tree to see if any hotspots are being touched by the mouse.
        If there are, those hotspots will have their data returned so that they can be added to the selected/clicked hotspots.
        This makes use of recursion (the subnodes make this possible.) (The same method gets called, but by different instances.)"""

        #If one of the subnodes is/isn't None, then they all are like that.
        if self._subnodes[0][0] != None:

            #Iterate through all of the subnode groups, because it's easier to group them up based off the the x and y planes.
            for subnodeGroup in self._subnodes:

                    #Iterate through each subnode within the current subnode group.
                    for subnode in subnodeGroup:
                        
                        #This checks to see if the mouse is over the current subnode
                        if Check_Collision(subnode._dimensions[0], subnode._dimensions[1], subnode._dimensions[2], subnode._dimensions[3], mousePos[0], mousePos[1]):

                            #print subnode._dimensions, "TreeNode._Get_Selected_Hotspot_Data(mousePos) is where this print is."
                            return subnode._Get_Selected_Hotspot_Data(mousePos)

        else:
            hotspotData = []

            #Iterate through the self._items to see if the mouse is colliding with one of the hotspots
            for i in xrange(len(self._items)-1,-1,-1):

                #rint Check_Collision(self._items[i][0], self._items[i][1], self._items[i][2], self._items[i][3], mousePos[0], mousePos[1])

                #Check to see if this item is colliding with the mouse!
                if Check_Collision(self._items[i][0], self._items[i][1], self._items[i][2], self._items[i][3], mousePos[0], mousePos[1]):

                    #This will append the data attached to the hotspot item, minus the dimensions of the hotspot.
                    hotspotData.append(self._items.pop(i))

                    #print hotspotData, "this shouldn't be None", "TreeNode._Get_Selected_Hotspot_Data(mousePos) is where this print is."
                    #print self._items

            return hotspotData          #if hotspotData != [] else None

        #Without this, an error got thrown every now and then. It was a very mysterious thing until I realized this needed to be here.
        #But if the _Check_Collision() method was working properly, I don't think this would be needed (doesn't hurt though.)
        return []


class Input_Manager(object):

    #The idea behind the storage for the inputs is that there exists a storage container (dKeyListeners, lHotspot) that only changes when a state change occurs.
    #And when one of these inputs is activated, the containers for the active inputs will begin to fill up (lActiveAction, lSelectedHotspots.)
    #So now the EntityManager only must check to see if there are any active inputs and all the rest is taken care of here.

    #This will store the past inputs that have been received IF each input was pressed within a certain time duration
    #(the time duration will be determined by checking the fTimeOfLastInput variable.)
    qPastInputs = []

    #This is for telling whether or not the multiple inputs that are being pressed are all released.
    iInputsToBeReleased = 0
    #Referring to the position within qPastInputs
    bGotoNextPos = False
    fTimeOfLastInput = 0.0

    #This will be handled by the _Mouse_Move() method and it will essentially hold the hotspots that are currently colliding with the mouse.
    #We only want to push the systems into the lActiveActions list once, but we then have to know if we have already done that.
    lSelectedHotspots = []

    #Actions or States that are active will be put into these lists.
    #Actions will be taken out once checked.
    #Actions can come from a key press, a selected hotspot, a clicked hotspot, a released key/hotspot click
    lActiveActions = []
    #States will stay until its associated key is released.
    #The only states so far will be from the OnPressed parts of the keys and hotspots
    #(although hotspots could (with some minor tweaks (adding a variable for the input type of the OnSelected functions)) have the same thing for their OnSelected parts.)
    lActiveStates = []

    #iKeyCode:(sInputType, (sPressedSystemFuncName, pressedEntities), (sReleasedSystemFuncName, releasedEntities))
    dKeyListeners = {}

    #iKeyCode:(sInputType, (sPressedSystemFuncName, pressedEntities), (sReleasedSystemFuncName, releasedEntities))
    dMouseButtonListeners = {}

    #This will hold all of the hotspots and the data associated with them.
    hotspotQuadTree = TreeNode(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    @staticmethod
    def _Empty_Inputs():
        """This is meant to basically set the Input_Manager back to its initial state (with empty containers.) This
        paves the way for a new state to be initialized."""
        del Input_Manager.qPastInputs[:]
        del Input_Manager.lSelectedHotspots[:]
        del Input_Manager.lActiveActions[:]
        del Input_Manager.lActiveStates[:]
        Input_Manager.dKeyListeners.clear()
        Input_Manager.dMouseButtonListeners.clear()
        Input_Manager.hotspotQuadTree._Reset_Node()

    @staticmethod
    def _Add_Key_Listener(sKeyCode, sInputType, sPressedSystemFuncName, lPressedEntities, sReleasedSystemFuncName, lReleasedEntities):
        """This adds either one or two system functions (with their dependent entities) to the list of key combinations we're looking for.
        Because the sKeyCodes variable is a string, we were able to """

        Input_Manager.dKeyListeners[sKeyCode] = (sInputType, (sPressedSystemFuncName, lPressedEntities), (sReleasedSystemFuncName, lReleasedEntities))

    @staticmethod
    def _Remove_Key_Listener(sKeyCode):
        """This currently does not work the way it should. If there are any key listeners that use the same system funcs andentities"""
        tKeyData = Input_Manager.dKeyListeners.get(sKeyCode,None)
        if tKeyData != None:
            if tKeyData[0] == "action":
                #Iterate through the ActiveActions and see if there exists (only when its active is it there) a remnant of this KeyListener element.
                for i in xrange(len(Input_Manager.lActiveActions)):
                    if (Input_Manager.lActiveActions[i][1][0] == tKeyData[1][0] and Input_Manager.lActiveActions[i][2][0] == tKeyData[2][0]) and (Input_Manager.lActiveActions[i][1][1] == tKeyData[1][1] and Input_Manager.lActiveActions[i][2][1] == tKeyData[2][1]):
                        del Input_Manager.lActiveActions[i]

            elif tKeyData[0] == "state":
                #Iterate through the ActiveStates and see if there exists (only when its active is it there) a remnant of this KeyListener element.
                for i in xrange(len(Input_Manager.lActiveStates)):
                    if (Input_Manager.lActiveStates[i][1][0] == tKeyData[1][0] and Input_Manager.lActiveStates[i][2][0] == tKeyData[2][0]) and (Input_Manager.lActiveStates[i][1][1] == tKeyData[1][1] and Input_Manager.lActiveStates[i][2][1] == tKeyData[2][1]):
                        del Input_Manager.lActiveStates[i]


            del Input_Manager.dKeyListeners[sKeyCode]
            
        else:
            pass
            #print iKeyCode, "does not exist in the Input_Manager's KeyListeners!"

    @staticmethod
    def _Add_Mouse_Listener(sKeyCode, sInputType, sPressedSystemFuncName, lPressedEntities, sReleasedSystemFuncName, lReleasedEntities):
        """This will be very similar to the Key_Listener, because both inputs are similar. This is centered around the mouse buttons though. And will not
        be apart of the combo system (they'll act independently :D.)"""
        
        #entities will contain [(sEntityType, sEntityName, sComponentName), (sEntityType, sEntityName, sComponentName), . . .]            
        Input_Manager.dMouseButtonListeners[sKeyCode] = (sInputType, (sPressedSystemFuncName, lPressedEntities), (sReleasedSystemFuncName, lReleasedEntities))
        
    @staticmethod
    def _Remove_Mouse_Listener(sKeyCode):
        """This currently does not work the way it should. If there are any key listeners that use the same system funcs andentities"""
        tKeyData = Input_Manager.dMouseButtonListeners.get(sKeyCode,None)
        if tKeyData != None:
            if tKeyData[0] == "action":
                #Iterate through the ActiveActions and see if there exists (only when its active is it there) a remnant of this KeyListener element.
                for i in xrange(len(Input_Manager.lActiveActions)):
                    if (Input_Manager.lActiveActions[i][1][0] == tKeyData[1][0] and Input_Manager.lActiveActions[i][2][0] == tKeyData[2][0]) and (Input_Manager.lActiveActions[i][1][1] == tKeyData[1][1] and Input_Manager.lActiveActions[i][2][1] == tKeyData[2][1]):
                        del Input_Manager.lActiveActions[i]

            elif tKeyData[0] == "state":
                #Iterate through the ActiveStates and see if there exists (only when its active is it there) a remnant of this KeyListener element.
                for i in xrange(len(Input_Manager.lActiveStates)):
                    if (Input_Manager.lActiveStates[i][1][0] == tKeyData[1][0] and Input_Manager.lActiveStates[i][2][0] == tKeyData[2][0]) and (Input_Manager.lActiveStates[i][1][1] == tKeyData[1][1] and Input_Manager.lActiveStates[i][2][1] == tKeyData[2][1]):
                        del Input_Manager.lActiveStates[i]


            del Input_Manager.MouseButtonListeners[sKeyCode]
            
        else:
            pass
            #print iKeyCode, "does not exist in the Input_Manager's KeyListeners!"
            
    @staticmethod
    def _Add_Hotspot(x, y, width, height,   \
                     sPressedInputType,     \
                     sSelectedSystemFuncName, lSelectedEntities,        \
                     sDeselectedSystemFuncName, lDeselectedEntities,    \
                     sPressedSystemFuncName, lPressedEntities,          \
                     sReleasedSystemFuncName, lReleasedEntities):

        Input_Manager.hotspotQuadTree._Add_Item((int(x), int(y), int(width), int(height), sPressedInputType, (sSelectedSystemFuncName, lSelectedEntities), (sDeselectedSystemFuncName, lDeselectedEntities), (sPressedSystemFuncName, lPressedEntities), (sReleasedSystemFuncName, lReleasedEntities)))
        
    @staticmethod
    def _Remove_Hotspot(x, y, width, height):
        pass

    @staticmethod
    def _Key_Input(iKeyCode, bPressed, currentTime):
        """This is for taking in data on the key that has been pressed (based off of sfml's enumeration of keys.) Its power is limited, but this will allow
        the game to have combos and simultaneous key presses. The only problem I see is that it won't allow a key to be pressed throughout the duration of the combo.
        And the subcombos that are a subset of a larger combo will be activated along with the larger combo (this could be an awesome feature, but also limiting.)"""

        #This will prevent unknown keys from doing things to the game.
        if iKeyCode != -1 and iKeyCode != 93:

            print "This %d keycode has been pressed"%(iKeyCode), bPressed

            if bPressed == True:
                #Check to see if this input was pressed within a duration of the last input.
                if Input_Manager.fTimeOfLastInput + 0.25 > currentTime:
                    #Check to see if the previous inputs haven't all been released yet.
                    if Input_Manager.bGotoNextPos == False:
                        #We'll just keep adding to the list of simultaneous key presses until all of these keys are released!
                        #We only ever add to the end of this list, so there's no point in using a variable.
                        Input_Manager.qPastInpus[-1].append(iKeyCode)

                    else:
                        #The last button has been released, so we append to the end!
                        Input_Manager.qPastInputs.append([iKeyCode])
                        
                        #Gotta reset this, because it will be set to True again when iKeyCode is released.
                        Input_Manager.bGotoNextPos = False

                    Input_Manager.fTimeOfLastInput = currentTime

                elif Input_Manager.iInputsToBeReleased != 0:
                    #Without this, the combo system's inputs that haven't been released yet won't get their OnReleased function executed.
                    return

                else:
                    #We'll have to reset our past inputs because the key being pressed isn't related to them.
                    del Input_Manager.qPastInputs[:]
                    #This also means that these variables should be reset as well.
                    Input_Manager.iInputsToBeReleased = 0
                    Input_Manager.bGotoNextPos = False

                    #This could be the start of a new combo!
                    Input_Manager.qPastInputs.append([iKeyCode])


                #This is suppose to end up looking like "/101.41.78./56./45.78."
                #Each "/" means that the following keys were all pressed at the same time (all keys that get pressed, until all of those keys are released, are grouped together.)
                #The "." separate the different keyIDs that exist in each group.
                sInputKey = ""

                for keyList in Input_Manager.qPastInputs:
                    sInputKey.append("/")
                    for iKeyID in keyList:
                        sInputKey.append(str(iKeyID)+".")

                #This checks our queue of inputs to see if it matches any of the ones in our dictionary.
                tKeyData = Input_Manager.dKeyListeners.get(sInputKeys,None)
                if tKeyData != None:
                    if tKeyData[0] == "action":
                        #tKeyData[1] is in this format [[0,1,2],[0,1,2],...]
                        #Each item of the overall list represents a single entity
                        Input_Manager.lActiveActions.append(tKeyData[1])

                    elif tKeyData[0] == "state":
                        Input_Manager.lActiveStates.append((sInputKeys, tKeyData[1]))
                    
            else:
                #A key was released!
                
                #Check to see if its time to change the position
                if (len(Input_Manager.qPastInputs) != 0 and len(Input_Manager.qPastInputs[-1]) == 1)    \
                   or Input_Manager.iInputsToBeReleased == 1:
                    #Signal to append to a new position when a new key is pressed, because the previous inputs have been released!
                    Input_Manager.bGotoNextPos = True

                    sInputKey = ""

                    for keyList in Input_Manager.qPastInputs:
                        sInputKey.append("/")
                        for iKeyID in keyList:
                            sInputKey.append(str(iKeyID)+".")
                
                    #We only want to signal the release function to be called when all of the keys are released from the last element.
                    tKeyData = Input_Manager.dKeyListeners.get(sInputKey,None)
                    if tKeyData != None:
                        if tKeyData[2][0] != None:
                            #All released inputs will be treated the same (because any input is only released once.)
                            #But if the input in question doesn't have data pertaining to what to do when the key is released,
                            #then there's no reason to add it to this list.
                            Input_Manager.lActiveActions.append(tKeyData[2])

                        #The first element of tKeyData is the InputType (action "a", state "s".)
                        if tKeyData[0] == "state":
                            #Take that keyCode out of the list of Active State inputs.
                            for i in xrange(len(Input_Manager.lActiveStates)):
                                if Input_Manager.lActiveStates[i][0] == sInputKey:
                                    del Input_Manager.lActiveStates[i]

                else:
                    #Check to see if this is the first to be released (with more to be expected.)
                    if Input_Manager.iInputsToBeReleased == 0:
                        #update that variable with the number of inputs that are needed to be released before we continure to the next position (minus one, because one input was released.)
                        Input_Manager.iInputsToBeReleased = len(Input_Manager.qPastInputs[-1])-1

                    else:
                        Input_Manager.iInputsToBeReleased -= 1

    @staticmethod
    def _Mouse_Input(iKeyCode, bPressed):
        """In this method, we'll be receving the key code of a pressed/released mouse button code and a boolean telling whether or not this button is pressed.
        We must pay attention to left-clicks especially. Because if we are colliding with a hotspot, then we must signal a function to be called."""

        if bPressed:
            #This checks to see if we are going to select one or more hotspots.
            #sf.Mouse.LEFT = 0
            if iKeyCode == 0 and len(Input_Manager.lSelectedHotspots) != 0:
                for indx in xrange(len(Input_Manager.lSelectedHotspots)-1,-1,-1):
                    if Input_Manager.lSelectedHotspots[indx][7][0] != None:
                        Input_Manager.lActiveActions.append(Input_Manager.lSelectedHotspots[indx][7])

            #In the event that a hotspot wasn't pressed, we will act like we are dealing with the key input (thus allowing multiple tile altering with the mouse clicks.)
            else:
                #This checks our queue of inputs to see if it matches any of the ones in our dictionary.
                tKeyData = Input_Manager.dMouseButtonListeners.get(str(iKeyCode),None)
                if tKeyData != None:
                    if tKeyData[0] == "action":
                        #tKeyData[1] is in this format [[0,1,2],[0,1,2],...]
                        #Each item of the overall list represents a single entity
                        Input_Manager.lActiveActions.append(tKeyData[1])

                    elif tKeyData[0] == "state":
                        Input_Manager.lActiveStates.append((str(iKeyCode), tKeyData[1]))

        else:
            #sf.Mouse.LEFT = 0
            if iKeyCode == 0 and len(Input_Manager.lSelectedHotspots) != 0:
                for indx in xrange(len(Input_Manager.lSelectedHotspots)-1,-1,-1):
                    if Input_Manager.lSelectedHotspots[indx][8][0] != None:
                        #This may be adding something to the active actions like the onPressed part above.
                        #But it adds a different function.
                        Input_Manager.lActiveActions.append(Input_Manager.lSelectedHotspots[indx][8])

            #This else allows us to activate a hotspot OR a button listener (hotspots have priority.)
            else:
                #This checks our queue of inputs to see if it matches any of the ones in our dictionary.
                tKeyData = Input_Manager.dMouseButtonListeners.get(str(iKeyCode),None)
                if tKeyData != None:

                    #There's no point in signaling for a non-existant function to be called
                    if tKeyData[2][0] != None:
                            #tKeyData[1] is in this format [[0,1,2],[0,1,2],...]
                            #Each item of the overall list represents a single entity
                            Input_Manager.lActiveActions.append(tKeyData[2])

                    if tKeyData[0] == "state":

                        #Iterate through the states to find the state that is done and needs taken out.
                        for indx in xrange(len(Input_Manager.lActiveStates)):

                            #Here we check to see if we've found the State item we're looking for.
                            if Input_Manager.lActiveStates[indx][0] == str(iKeyCode):
                                
                                #This takes the previous state function out, because the key is now released.
                                Input_Manager.lActiveStates.pop(indx)
                                
                                #There's no point in signaling for a non-existant function to be called
                                if tKeyData[2][0] != None:
                                    #But then we signal to do an action function.
                                    Input_Manager.lActiveActions.append(tKeyData[2])



    @staticmethod
    def _Mouse_Has_Moved(tMousePos):
        """This informs that the mouse has moved and to a position represented by a tuple of integers."""

        #This will iterate through all of the hotspots that are colliding with the mouse at this point in time.
        for tSelectedHotspot in Input_Manager.hotspotQuadTree._Get_Selected_Hotspot_Data(tMousePos):
            #print "Hotspot Selected!"

            if tSelectedHotspot[5][0] != None:
                #This appends strictly the OnSelected data of the hotspot to the list of active actions.
                #This schedules the OnSelected function to be executed once and only once (the data got popped out of the QuadTree!)
                Input_Manager.lActiveActions.append(tSelectedHotspot[5])
                #It will be important to put these back into the QuadTree (they get taken out temporaryily while they are being selected, prevents having to check collision each time.)

            Input_Manager.lSelectedHotspots.append(tSelectedHotspot)


        #This iterates through all of the hotspots that are supposedly selected (the mouse just moved.)
        for indx in xrange(len(Input_Manager.lSelectedHotspots)-1,-1,-1):

            #print "Checking the selected hotspots for being selected..."
            #This will check to see if the mouse isn't colliding with the current hotspot anymore.
            if not Check_Collision(Input_Manager.lSelectedHotspots[indx][0], Input_Manager.lSelectedHotspots[indx][1], Input_Manager.lSelectedHotspots[indx][2], Input_Manager.lSelectedHotspots[indx][3], \
                                                tMousePos[0], tMousePos[1]):

                if Input_Manager.lSelectedHotspots[indx][6][0] != None:
                    #Now we signal the deselected function to activate
                    Input_Manager.lActiveActions.append(Input_Manager.lSelectedHotspots[indx][6])
                    
                #And then add the hotspot back into the quad tree while simultaneously taking it out of the SelectedHotspots list.
                Input_Manager.hotspotQuadTree._Add_Item(Input_Manager.lSelectedHotspots.pop(indx))

                #print "Hotspot has been deselected!"


    @staticmethod
    def _Get_Active_Inputs():
        """This will return a list of tuples containing the key code and the entityType that belongs to the input's entity."""
        #This saves a copy of all of the active inputs (we're deleting the contents of the lActiveActions list.)
        lActiveInputs = [Input_Manager.lActiveActions[i] for i in xrange(len(Input_Manager.lActiveActions))]  \
                        + [Input_Manager.lActiveStates[i][1] for i in xrange(len(Input_Manager.lActiveStates))]

        #Actions only need to occur once, so we take them out after they've been checked for existence.
        del Input_Manager.lActiveActions[:]
        return lActiveInputs
