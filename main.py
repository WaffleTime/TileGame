from math import ceil
#This is so that we can import a module to be used within the ChangeState() func.
import importlib
import sfml as sf
from elementtree.ElementTree import parse
import config
import entities
from staticInput import Input_Manager
from systems import System_Manager
import assets

class Entity_Manager(object):
    def __init__(self):
        #sEntityType:(sEntityName:entity)
        self._dEntities = {}

    def _Empty_Entity_Containers(self):
        """This is for cleaning up the Entity Containers for when we need to change
        the buttons for the next state."""

        #If this was in C++ (Python may be fine without the proposal below)
        #I think it'd be good to loop through all of the entities and give each of them to a system that would
        #check to see if their component dictionaries contained a component that needs cleaned up a special way.
        
        self._dEntities.clear()

    def _Add_Entity(self, entity):
        """This will add entities into our dictionary of lists of entities.
        @param entity This should be an actual instance of the Entity class. So it
            holds components and that's about it."""

        if self._dEntities.get(entity._Get_Type(), None) == None:
            #If there wasn't already a dictionary, then we'll make one
            self._dEntities[entity._Get_Type()] = {}

        #This will overwrite or create a new entity of the given name.
        self._dEntities[entity._Get_Type()][entity._Get_Name()] = entity

    def _Remove_Entity(self, sEntityTypeName, sEntityName):
        """When an entity expires it will be removed with this."""
        #This just prevents errors from occuring in the dictionary accessing.
        if self._dEntities.get(sEntityTypeName,None) != None:
            self._dEntities[sEntityTypeName].pop(sEntityName)

    def _Get_Entity(self, sEntityTypeName, sEntityName):
        """This is for retrieving entities from the dictionary. It so far
        is only used for the System functions in the ChangeState() function."""

        if self._dEntities.get(sEntityTypeName,None) != None:
            
            return self._dEntities[sEntityTypeName][sEntityName]

    def _Call_System_Func(self, sSystemFuncName, lEntities):
        """This will call a system function from the systems.py file. And it will provide the appropriate entities that are needed to be passed to the function.
        This will also return a variable from the system function.
        @param sSystemFuncName This is the name of the System function that is to be called.
        @param lEntities This is a list of tuples containing information on the entities
            that will have to be passed to the system function that is to be called. This allows
            systems to act upon entities, so the components can be changed."""

        #If one entity to pass to the systemFunc
        #lEntities == [(sEntityType, sEntityName, sComponentName)]
        #If two entities to pass to the systemFunc
        #lEntities == [(sEntityType, sEntityName, sComponentName),(sEntityType, sEntityName, sComponentName)]
        
        module = importlib.import_module('systems')
        systemFunc = getattr(module, sSystemFuncName)

        #I'm sure that this is suppose to be an empty list
        if lEntities == []:

            return systemFunc()

        else:
            #sComponentName:entityInstance
            dEntities = {}

            for indx in xrange(len(lEntities)):
                
                #Test to see if this sEntityType and sEntityID even exists.
                if self._dEntities.get(lEntities[indx][0],None) != None and self._dEntities[lEntities[indx][0]].get(lEntities[indx][1], None) != None:

                    #This grabs the entity and stores it into the new dictionary we just made
                    dEntities[lEntities[indx][2]] = self._dEntities[lEntities[indx][0]][lEntities[indx][1]]
                else:
                    print "EntityType: %s, EntityName: %s doesn't exist in the EntityManager's container of entities!" % (lEntities[indx][0], lEntities[indx][1])

            return systemFunc(dEntities)        

    def _Input_Update(self):
        """This will essentially execute all of the system functions that it is told to by the Input_Manager. And it will return the new lNextState variable, which
        should be ["NULL","NULL"] if a state change isn't needed."""

        #Loop through all of the inputs that are active according to the Input_Manager class
        for (sSystemFuncName, lEntities) in Input_Manager._Get_Active_Inputs():

            sNextState = self._Call_System_Func(sSystemFuncName, lEntities)

            #print sNextState

            #Only strings are allowed to be returned from the system functions and only if the state needs to be changed.
            #Otherwise, we'll just keep calling system functions and eventually return something that makes no state change occur.
            if sNextState != "NULL,NULL":

                return sNextState.split(',')

        return ["NULL","NULL"]

    def _Logic_Update(self, timeElapsed):
        """This method is simple, but important. It signals the Entities within our dictionary of entities to update themselves with only the timeElapsed as new data.
        NOTE: This may be able to be put into the Entity_Manager class instead of here."""

        #Before updating any of the entities, we need to call all of the active system functions (providing the associated entities as arguments.)

        for (sSystemFuncName, lEntities) in System_Manager._Get_Active_Systems():
            self._Call_System_Func(sSystemFuncName, lEntities)
            

        #This block iterates through all of the entities in our dictionary of dictionaries and signals each to update itself.
        for (sEntityType, dEntities) in self._dEntities.items():

            for (sEntityName, entity) in dEntities.items():

                #Check to see if the Entity is expired
                if entity._Is_Expired():
                    entity._On_Expire()
                    self._Remove_Entity(entity._Get_Type(), entity._Get_Name())

                entity._Update(timeElapsed)


    def _Render_Update(self, pWindow, pWindowView):
        #print "Render Update!"

        pWindow.clear(sf.Color.BLACK)

        #This block iterates through all of the entities in our dictionary of dictionaries and signals each to update itself.
        for (sEntityType, dEntities) in self._dEntities.items():
            for (sEntityName, entity) in dEntities.items():
                entity._Render(pWindow, pWindowView)

def AssembleEntityInfo(root, sSystemRoot=None):
    """This will assemble the entity info for possibly several entities that are associated with a system call.
    This is meant to automate a way that we retrieve and assemble entity information for our xml files.
    @param root This is the root of some parsed xml, this object comes from the ElementTree library.
        The specific root object is of a sub-tree of the original xml data, only important
        entities will be contained in this sub-tree.
    @param sSystemRoot If this is specified, then it means that this is a section that needs to be looked in
        to find the entity data we want to return. The section is a child of the root.
    @return A list of entity data that can be used by the InputManager and SystemManager."""
    lEntities = []

    if sSystemRoot == None:
        for entity in root.findall("entity"):
            lEntities.append((entity.find("entityType").text, entity.find("entitytName").text, entity.find("componentName").text))
            
    elif root.find(sSystemRoot) != None:       
        for entity in root.find(sSystemRoot).findall("entity"): 
            lEntities.append((entity.find("entityType").text, entity.find("entitytName").text, entity.find("componentName").text))

    return lEntities


def ChangeState(lCurState, lNxtState, windView, EntManager, AstManager):
    """This function is passed a couple lists representing the info on the different levels of this game's
    hierarchical finite state machine. This function essentially generically sets up the Entity and Asset Managers
    based off of data that can be retreived from xml files.
    @param lCurState This list contains the information on which state the program is in and it takes acount into
        sub-states. So each element of the list is a sub-state of the previous element.
    @param lNxtState This list contains the information on which state the program is to be switched to and it takes acount into
        sub-states. So each element of the list is a sub-state of the previous element.
    @param windView This is SFML's View object and allows us to zoom in on the what would be shown in the window. This
        essentially just gives us the option to zoom in on the stuff visible for a certain state (can be specified in xml data.)
    @param EntManager This is the entity manager and is for loading entities into the game based on the state being switched to.
        The xml data tells which entities need to be loaded for what state.
    @param AstManager This is the asset manager and it is for loading in assets that are needed by entities. The xml data
        specifies what assets are to be fetched and used for the assembling of each entity. Once an asset is fetched once,
        it won't need to be loaded the second time because it's stored in the AstManager."""

    print "NEW STATE!", lNxtState
    #The data will lie within the nextState[0]+".txt" file and the nextState[1] element within that elemthe ent.
    tree = parse("StateData/StateInit.xml")
    
    #The root element and the element containing the entities we need will be using this variable.
    root = tree.getroot()

    if root.find(lNxtState[0]) != None:
        #This changes the node to the one that represents the state we're switching to.
        root = root.find(lNxtState[0]).find(lNxtState[1])
        
        if root == None:
            print "There was a problem finding %s in the StateInit.xml file."%(lNxtState[1])
    else:
        print "There was a problem finding %s in the StateInit.xml file."%(lNxtState[0])

    #This will reset the windowView's dimensions within the actual window with respect to the new state
    windView.reset(sf.FloatRect(int(int(root.find('viewWidth').text)//4), \
                int(int(root.find('viewHeight').text)//4),   \
                int(int(root.find('viewWidth').text)//2),    \
                int(int(root.find('viewHeight').text)//2)))

    #This clears all of the things that in the game since the last state
    EntManager._Empty_Entity_Containers()
    AstManager._Empty_Assets()
    Input_Manager._Empty_Inputs()
    System_Manager._Empty_Systems()

    for entity in root.findall('Entity'):

        entityInstance = None

        #This checks to see if there is a function that exists that will assemble this entity.
        if entity.find('assembleFunc') != None:

            #This will hold all of the attributes needed to assemble the entity (using the xml files to get the data later on.)
            dEntityAttribs = {}

            #This will loop through all of the attribute names for each entity.
            for attrib in entity.find('Attributes').getiterator():
                
                #Check to see if this is a sound for the entity!
                if attrib.tag == 'Sound':
                    #THis will start a new list of Sounds if we haven't already loaded a sound into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}

                    #Query the AssetManager for a sound that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = AstManager._Get_Sound(attrib.attrib['name'], attrib.text)

                elif attrib.tag == 'Music':

                    #THis will start a new list of Musics if we haven't already loaded a sound into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}

                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = AstManager._Get_Music(attrib.attrib['name'], attrib.text)

                #Check to see if this is a texture for the entitititity.
                elif attrib.tag == 'Texture':

                    #THis will start a new list of Textures if we haven't already loaded a sound into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}

                    #Query the AssetManager for a texture that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = AstManager._Get_Texture(attrib.attrib['name'], attrib.text)

                #Check to see if this is a RenderState for the entitititity.
                elif attrib.tag == 'RenderState':

                    #THis will start a new list of sf.RenderStates if we haven't already loaded a sound into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}

                    #Query the AssetManager for a sf.RenderState that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = AstManager._Get_Render_State(attrib.attrib['name'], attrib.text)


                #Check to see if this is a font for the entitititity.
                elif attrib.tag == 'Font':

                    #THis will start a new list of Fonts if we haven't already loaded a sound into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}

                    #Query the AssetManager for a font that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = AstManager._Get_Font(attrib.attrib['name'], attrib.text)

                else:
                    #Anything else will just be put in the dictionary as an attribute
                    dEntityAttribs[attrib.tag] = attrib.text

            module = importlib.import_module('entities')

            assembleFunc = getattr(module, entity.find('assembleFunc').text)
               
            #Here we're using the Assemble*() function associated with the name of this entity to assemble the entity so that
            #we can add it to the EntityManager.
            #And all Assemble*() functions will use the same arguments(using a dictionary to allow dynamic arguments.)
            entityInstance = assembleFunc(entity.attrib['name'], entity.attrib['type'], dEntityAttribs)

        else:
            #Here we will add in a default entity instance.
            entityInstance = entities.Entity(entity.attrib['name'], entity.attrib['type'],{})
        
        #THis adds in the components that exist in the xml file for this entity (it allows custom/variations of entities to exist.)
        for component in entity.findall('Component'):

            #These are for getting the actual 
            module = importlib.import_module('components')

            componentClass = getattr(module, component.attrib['name'])

            #This will add in a component into the entity we just created.
            #And note that it is giving the component a dictionary of the data in the xml files.
            entityInstance._Add_Component(componentClass({DataTag.tag: DataTag.text for DataTag in component.getiterator()}))

        EntManager._Add_Entity(entityInstance)

            
    #Each one of these nodes will be an input that will be initialized for the state that is being loaded (and a multitude of kinds.)
    for inpoot in root.findall("Input"):

        #Check to see if this input's type is a hotspot.
        if inpoot.attrib["type"] == "hotspot":
            Input_Manager._Add_Hotspot(inpoot.find("x").text, inpoot.find("y").text, inpoot.find("width").text, inpoot.find("height").text, \
                                       inpoot.find("OnPressed").find("type").text if inpoot.find("OnPressed") != None else None,    \
                                       inpoot.find("OnSelected").find("system").text if inpoot.find("OnSelected") != None else None,    \
                                       AssembleEntityInfo(inpoot, "OnSelected"), \
                                       inpoot.find("OnDeselected").find("system").text if inpoot.find("OnDeselected") != None else None,    \
                                       AssembleEntityInfo(inpoot, "OnDeselected"), \
                                       inpoot.find("OnPressed").find("system").text if inpoot.find("OnPressed") != None else None,    \
                                       AssembleEntityInfo(inpoot, "OnPressed"), \
                                       inpoot.find("OnReleased").find("system").text if inpoot.find("OnReleased") != None else None,   \
                                       AssembleEntityInfo(inpoot, "OnReleased"))

        #Check to see if thisinput's type is a action.
        elif inpoot.attrib["type"] == "key":
            #This will add a key_Listener to our Input_Manager given the attribute data from the inpoot elemenet from the xml file.
            Input_Manager._Add_Key_Listener(inpoot.find("key").text,    \
                                            inpoot.find("OnPressed").find("type").text if inpoot.find("OnPressed") != None else None,  \
                                            inpoot.find("OnPressed").find("system").text if inpoot.find("OnPressed") != None else None,   \
                                            AssembleEntityInfo(inpoot, "OnPressed"),    \
                                            inpoot.find("OnReleased").find("system").text if inpoot.find("OnReleased") != None else None,   \
                                            AssembleEntityInfo(inpoot, "OnReleased"))

        elif inpoot.attrib["type"] == "mouse":
            pass

    #These are the systems that are relevant to this state and they will be added into the System_Queue class.
    for system in root.findall("System"):

        #dEntities = {}

        #for entity in system.findall("entity"):

            #dEntities[entity.find("componentName")] = EntManager._Get_Entity(entity.find("entityType"), entity.find("entityName"))

        #This will load a system into the System_Queue and then it will be activated next update.
        System_Manager._Add_System(system.find("type").text, system.find("systemFunc").text,  AssembleEntityInfo(system))
        
            
    #Now we gotta update the state variables so that we aren't signaling to change states anymore
    for i in xrange(len(lCurState)):
        lCurState[i] = lNxtState[i]
        lNxtState[i] = "NULL"


def Init():
    """This will setup the window and whatever needs setup (just once) at the start of the program."""
    wind = sf.RenderWindow( sf.VideoMode( config.WINDOW_WIDTH, config.WINDOW_HEIGHT ), "CS CLUB PROJECT!" )

    #This makes the background of the screen Black.
    wind.clear(sf.Color.BLACK)

    wind.framerate_limit = 50

    windView = sf.View()

    return wind, windView
    


def main():
    #Initialize the window and windowView (the windowView won't be setup until the state changes!)
    window, windowView = Init()
    
    #These variables will track our position within the game.
    lCurrentState = ["NULL","NULL"]
    lNextState = ["Menu","MainMenu"]

    #This will be updated when we change to a state.
    EntityManager = Entity_Manager()

    #The AssetManager will be used by ChangeState in order to retrieve sounds/textures for a particular type of entity.
    AssetManager = assets.Asset_Manager()

    ChangeState(lCurrentState, lNextState, windowView, EntityManager, AssetManager)

    timer = sf.Clock()
    
    SKIP_TICKS = 1/config.TICKS_PER_SEC
    MAX_FRAMESKIP = 5
    
    iLoops = None
    fNextGameTick = timer.elapsed_time

    #This will be False if the player clicks outside of the program's window and "pause" the program
    windowIsActive = True
    
    bQuit = False
    while not bQuit:
    
        #This will loop through all of the events that have been triggered by player input
        for event in window.iter_events():

            if event.type == sf.Event.MOUSE_MOVED:
                Input_Manager._Mouse_Has_Moved(window.convert_coords(event.x,event.y))

            elif event.type == sf.Event.TEXT_ENTERED:
                Input_Manager._Key_Input(event.unicode, True, timer.elapsed_time)
            
            elif event.type == sf.Event.KEY_PRESSED:
                Input_Manager._Key_Input(event.code, True, timer.elapsed_time)
                
            elif event.type == sf.Event.KEY_RELEASED:
                Input_Manager._Key_Input(event.code, False, timer.elapsed_time)
            
            elif event.type == sf.Event.MOUSE_BUTTON_PRESSED:
                Input_Manager._Mouse_Input(event.button, True)
            
            elif event.type == sf.Event.MOUSE_BUTTON_RELEASED:
                Input_Manager._Mouse_Input(event.button,False)
                
            elif event.type == sf.Event.LOST_FOCUS:
                windowIsActive = False

            elif event.type == sf.Event.GAINED_FOCUS:
                windowIsActive = True
                
            elif event.type == sf.Event.CLOSED:
                for stateIndx in xrange(len(lNextState)):                     
                    lNextState[stateIndx] = "QUIT"
                bQuit = True


        iLoops = 0  #A counter for the amount of game update loops that are made in sucession whilst skipping rendering updates.
        
        #This loop will start if it is time to commence the next update and will keep going if we are behind schedule and need to catch up.
        while timer.elapsed_time > fNextGameTick and iLoops < MAX_FRAMESKIP:
    
            #This makes the program so that it basically pauses all of its game updates when a user clicks outside of the window. And it waits until the user clicks on the window.
            if windowIsActive:

                #We don't want to change lNextState if the game has been set to QUIT
                if not bQuit:
                
                    #lNextState will contain "NULL"s when no state change is signaled
                    #lNextState will have all of its elements change when switching to a new state.
                    lNextState = EntityManager._Input_Update()

                    #Check to see if we have signaled to quit the game thus far
                    if lNextState[0] == "QUIT":
                        bQuit = True

                    #If one of the lNextState elements is changed, they all are (just how it goes.)
                    if lNextState[0] != "NULL" and lNextState[0] != "QUIT":
                        ChangeState(lCurrentState, lNextState, windowView, EntityManager, AssetManager)

                #Finally after we've handled input and have correctly adjusted to the nextState (in most cases it won't happen,)
                #we can then update our game's model with stuff that will happen in the respective state with each game update.
                if not bQuit:
                    EntityManager._Logic_Update(timer.elapsed_time - fNextGameTick)           #This updates our model depending on what is going on in the current state

            #If we have received a quit signal, we should stop our loop and quit the game!
            if bQuit:
                break
                
            iLoops += 1
            fNextGameTick += sf.Time(seconds=SKIP_TICKS)

        EntityManager._Render_Update(window, windowView)
        window.display()

    #This closes our RenderWindow!
    window.close()


#If this file was ran as the main, then we will call the main (if it was included in another file, this would prevent main() from being called.)
if __name__ == '__main__':
    main()
