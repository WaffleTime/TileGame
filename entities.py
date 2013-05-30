import os
import sfml as sf
import components
import config
from PriorityQueue import PriorityQueue as PQ

#Maybe we can include the Components file here and then have
#assemblage functions for creating common entities.

def Assemble_Text_Box(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This assembles a box with text in it!"""
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    #The first argument represents the ID of the component with respect to its type (multiple components of a single type need to have different IDs.)
    entity._Add_Component(components.Box({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height']}))
    entity._Add_Component(components.Text_Line({'componentID': "0", 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height'], 'text': attribDict['text'], 'font': attribDict["Font"]["Asman"]}))

    return entity

def Assemble_Button(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This assembles a box with text in it! And sets up some other
    components that'll store important information we might need later."""
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})
    
    entity._Add_Component(components.Box({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height']}))
    entity._Add_Component(components.Text_Line({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height'], 'text': attribDict['text'], 'font': attribDict['Font']["Asman"]}))
    entity._Add_Component(components.Flag({'componentID': '0', 'flag': False}))

    return entity

def Assemble_Player(sEntityName, sEntityType, iDrawPriority, attribDict):
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    entity._Add_Component(components.Animated_Sprite({"componentID":"mainSprite",                \
                                                      "FrameWidth":attribDict["FrameWidth"],     \
                                                      "FrameHeight":attribDict["FrameHeight"],   \
                                                      "Delay":attribDict["Delay"],               \
                                                      "WindPos":attribDict["WindPos"],          \
                                                      "Texture":attribDict["Texture"]}))

    entity._Add_Component(components.Position({"componentID":"WindPos",        \
                                               "position":attribDict["WindPos"].split(",")}))

    return entity

def Assemble_Chunk(sEntityName, sEntityType, iDrawPriority, attribDict):
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    dMeshData = {"componentID":"0"}

    #Iterating through the attribDict items
    for (attribName, attrib) in attribDict.items():
        #This checks to see if the current item is
        #   for the Mesh component.
        if attribName[0:9] == "TileAtlas":
            #This will add in the Texture objects
            #   defined by SFMl. This Texture object
            #   points to a Texture object within
            #   the AssetManager.
            dMeshData[attribName] = attrib

    entity._Add_Component(components.Mesh(dMeshData))

    entity._Add_Component(components.Position({"componentID":"WorldPos", "position":attribDict['WorldPos'].split(',')}))
    entity._Add_Component(components.Position({"componentID":"WindowPos", "position":attribDict['WindowPos'].split(',')}))

    entity._Add_Component(components.Flag({"componentID":"IsEmpty", "flag":True}))
    entity._Add_Component(components.Flag({"componentID":"IsLoaded", "flag":False}))

    tileList = components.List({"componentID":"Tiles"})

    for row in xrange(config.CHUNK_TILES_HIGH):
        #Adds in a list for each row of the tiles
        tileList._Add(components.List({"componentID":"Tiles"}))
        
        for col in xrange(config.CHUNK_TILES_WIDE):
            #Adds in a list for each col of the tiles
            tileList[row]._Add(components.List({"componentID":"Tiles"}))
            for depth in xrange(config.CHUNK_LAYERS):
                #Then adds in a tile, for each layer that exists, into
                #   each 2d tile position in this chunk.
                tileList[row][col]._Add( components.Tile({"componentID":str(row)+","+str(col)+","+str(depth)}) )

    entity._Add_Component(tileList)

    return entity


def Assemble_Chunk_Manager(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This will return an Entity object that contains a list of lists of lists of tiles,
    some world coordinates, the number of chunks in the screen, and all that stuff that is
    needed in order to manager a chunks of tiles (except for the textures, those are already
    taken care of.)"""
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    #Notice that the ChunkDataDir is prefixed by the directory that this file is in.
    entity._Add_Component(components.Misc({"componentID":"ChunkDataDir", "storage":os.getcwd()+attribDict["ChunkDataDir"]}))

    entity._Add_Component(components.Position({"componentID":"WorldPos", "position":attribDict["WorldPos"].split(',')}))
    entity._Add_Component(components.Position({"componentID":"ChunksInWind", "position":attribDict["ChunksInWind"].split(",")}))
    entity._Add_Component(components.Flag({"componentID":"VisibilityUpdate", "flag":False}))

    entity._Add_Component(components.Dictionary({"componentID":"ChunkDict"}))

    entity._Add_Component(components.List({"componentID":"LoadList"}))
    entity._Add_Component(components.List({"componentID":"RebuildList"}))
    entity._Add_Component(components.List({"componentID":"UnloadList"}))
    entity._Add_Component(components.List({"componentID":"FlagList"}))
    entity._Add_Component(components.Render_List({"componentID":"RenderList"}))

    lWorldPos = attribDict["WorldPos"].split(",")

    lChunksInWindow = attribDict["ChunksInWind"].split(",")


    #This will strictly assemble the chunks around the outside of the chunks on the screen (the first items in the loadList get loaded last, so we add these first!)
    #This only will loop through the chunks to the left and right of the screen.
    for i in xrange( int(lWorldPos[0])-1, int(lWorldPos[0]) + int(lChunksInWindow[0])+1 ):
        for j in xrange( int(lWorldPos[1])-1, int(lWorldPos[1]) + int(lChunksInWindow[1])+1, int(lChunksInWindow[1])+1 ):

            dChunkData = {"WorldPos":"%d,%d"%(i,j), \
                          "WindowPos":str(i - int(lWorldPos[0]))+","+str(j - int(lWorldPos[1]))}

            #Iterating through the dictionary of Texture items within
            #   an element of the attribDict. These textures are
            #   the tileAtlas' and are for the Chunks Mesh component.
            for (attribName, attrib) in attribDict["RenderState"].items():
                
                #This checks to see if the current item is
                #   for the Mesh component.
                if attribName[0:9] == "TileAtlas":
                    #This will add in the Texture objects
                    #   defined by SFMl. This Texture object
                    #   points to a Texture object within
                    #   the AssetManager.
                    dChunkData[attribName] = attrib


            entity._Get_Component("DICT:ChunkDict")._Add( "%d,%d"%(i,j),                        \
                                                          Assemble_Chunk( "%s,%s" % (i, j),     \
                                                                          "Chunk",              \
                                                                          iDrawPriority,        \
                                                                          dChunkData ) )

            pChunk = entity._Get_Component("DICT:ChunkDict")._Get("%d,%d"%(i,j))

            entity._Get_Component("LIST:LoadList")._Add(pChunk)

    #This does the same thing as the previous loop, but with different chunks (above the screen and below the screen.)
    for i in xrange( int(lWorldPos[0])-1, int(lWorldPos[0]) + int(lChunksInWindow[0])+1, int(lChunksInWindow[0])+1 ):
        for j in xrange( int(lWorldPos[1])-1, int(lWorldPos[1]) + int(lChunksInWindow[1])+1):

            dChunkData = {"WorldPos":"%d,%d"%(i,j), \
                          "WindowPos":str(i - int(lWorldPos[0]))+","+str(j - int(lWorldPos[1]))}

            #Iterating through the dictionary of Texture items within
            #   an element of the attribDict. These textures are
            #   the tileAtlas' and are for the Chunks Mesh component.
            for (attribName, attrib) in attribDict["RenderState"].items():
                #This checks to see if the current item is
                #   for the Mesh component.
                if attribName[0:9] == "TileAtlas":
                    #This will add in the Texture objects
                    #   defined by SFMl. This Texture object
                    #   points to a Texture object within
                    #   the AssetManager.
                    dChunkData[attribName] = attrib


            entity._Get_Component("DICT:ChunkDict")._Add( "%d,%d"%(i,j),                        \
                                                          Assemble_Chunk( "%s,%s" % (i, j),     \
                                                                          "Chunk",              \
                                                                          iDrawPriority,        \
                                                                          dChunkData ) )

            pChunk = entity._Get_Component("DICT:ChunkDict")._Get("%d,%d"%(i,j))

            entity._Get_Component("LIST:LoadList")._Add(pChunk)

    #This will assemble the chunks that are inside of the screen (these chunks need loaded first and their meshes built.)
    for i in xrange(int(lWorldPos[0]), int(lWorldPos[0]) + int(lChunksInWindow[0])):
        for j in xrange(int(lWorldPos[1]), int(lWorldPos[1]) + int(lChunksInWindow[1])):

            dChunkData = {"WorldPos":"%d,%d"%(i,j), \
                          "WindowPos":str(i - int(lWorldPos[0]))+","+str(j - int(lWorldPos[1]))}

            #Iterating through the dictionary of Texture items within
            #   an element of the attribDict. These textures are
            #   the tileAtlas' and are for the Chunks Mesh component.
            for (attribName, attrib) in attribDict["RenderState"].items():
                #This checks to see if the current item is
                #   for the Mesh component.
                if attribName[0:9] == "TileAtlas":
                    #This will add in the Texture objects
                    #   defined by SFMl. This Texture object
                    #   points to a Texture object within
                    #   the AssetManager.
                    dChunkData[attribName] = attrib


            entity._Get_Component("DICT:ChunkDict")._Add( "%d,%d"%(i,j),                        \
                                                          Assemble_Chunk( "%s,%s" % (i, j),     \
                                                                          "Chunk",              \
                                                                          iDrawPriority,        \
                                                                          dChunkData ) )

            pChunk = entity._Get_Component("DICT:ChunkDict")._Get("%d,%d"%(i,j))

            entity._Get_Component("LIST:LoadList")._Add(pChunk)

            entity._Get_Component("LIST:RebuildList")._Add(pChunk)


    return entity


class Entity(object):
    def __init__(self, sEntityName, sEntityType, iDrawPriority, dComponents):
        #The id is mostly for debugging purposes.
        self._sName = sEntityName
        self._sType = sEntityType

        self._iDrawPriority = iDrawPriority

        #componentName:component
        #Drawable components that are in the dComponents dictionary will have a pointer to them in this list.
        self._dComponents = {}

        #These drawable components will be drawn with respect to the
        #   view of the game.
        self._lViewDrawables = []
        
        #These drawable components will be drawn with respect to the
        #   screen, the view is independent.
        self._lScreenDrawables = []

        #Updatable components that hold pointer variables that point to the updatable components in the dComponents dictionary.
        self._lUpdatables = []

        self._bExpired = False

        for key in dComponents.keys():
            self._Add_Component(dComponents.pop(key))


    def _Add_Component(self, componentInstance):
        """This takes in an instance of a class that inherits from the Component class
        and then it adds that instance into the list of components for this particular entity."""

        #print "Componet being added to %s entity."%(self._sName)
        #print componentInstance
        
        self._dComponents[componentInstance._Get_Name()] = componentInstance

        #These if statements will save a pointer of the same variable as in dComponents if True.

        if componentInstance._Get_Updatable():
            self._lUpdatables.append(componentInstance)

        if componentInstance._Get_View_Drawable():
            self._lViewDrawables.append(componentInstance)

        elif componentInstance._Get_Screen_Drawable():
            self._lScreenDrawables.append(componentInstance)

    def _Remove_Component(self, sCompName):
        """This searches through our list of components for the component with
        the specified ID and then removes it from the list."""
        del self._dComponents[sCompName]

    def __len__(self):
        return len(self._dComponents)

    def _Get_Draw_Priority(self):
        return self._iDrawPriority
    
    def _Get_Name(self):
        """This is for accessing the names of the entities."""
        return self._sName

    def _Get_Type(self):
        """This is essential information needed to locate the entity within the Entity_Manager's entity dictionary."""
        return self._sType

    def _Get_Component(self, sCompName):
        """This will return the instance of a component that contains
        the specified ID."""
        return self._dComponents[sCompName]

    def _Update(self, timeElapsed):
        """This will update the updatable components within the dComponents dictionary by indirectly updating the pointer variables within lUpdatables."""

        for i in xrange(len(self._lUpdatables)):

            #This calls the Updatable component's _Update() method.
            self._lUpdatables[i]._Update(timeElapsed)

    def _Render(self, renderWindow, windowView):
        """This will render the drawable components within the dCOmponents dictionary by indirectly rendering the pointer variables within lDrawables."""

        #print "These are the drawable components that are being drawn."
        #print self._lViewDrawables
        #print self._lScreenDrawables

        renderWindow.view = windowView
        
        for i in xrange(len(self._lViewDrawables)):

            #This calls the Drawable component's _Render() method.
            self._lViewDrawables[i]._Render(renderWindow)

        renderWindow.view = renderWindow.default_view

        for i in xrange(len(self._lScreenDrawables)):

            #This calls the Drawable component's _Render() method.
            self._lScreenDrawables[i]._Render(renderWindow)

    def _Set_Expired(self, bExpired):
        """This is for signaling an entity to be removed from the Entity_Manager's dictionary of entities."""
        self._bExpired = bExpired

    def _Is_Expired(self):
        """This is for checking to see if we should delete the entity or not."""
        return self._bExpired

    def _On_Expire(self):
        """This is what is to be done when the entity is removed. It's almost like a destructor.
        I don't know what to use it for though. Maybe for removing system functions that are associated with this entity.
        That would require the entity to store something that will tell us the associated system functions."""
        pass



        

class Entity_PQueue(Entity):
    """Like the name says, this will store Entities. And it will update/render those entities accordingly."""
    def __init__(self, sName, sType, iDrawPriority, dComponents):

        #This takes all of the entities out of the dComponents
        dEntities = dComponents.pop("entity", {})

        print "These are the entities that are being loaded into the Entity_PQueue"
        print dEntities
        
        Entity.__init__(self, sName, sType, iDrawPriority, dComponents)

        #This orders the entities so that the ones with the highest draw
        #   priority will be first in the list (highest priority is 0.)
        self._pqEntities = PQ(dEntities.values())

    def _Add_Entity(self, entity):
        """This will add entities into our dictionary of lists of entities.
        And it will also add the Entity to the PriorityQueue so that it can be drawn.
        @param entity This should be an actual instance of the Entity class. So it
            holds components and that's about it.
        @param iPriority This is the draw priority for the Entity that it being
            added. Zero is the highest draw priority (gets drawn first,) -1 means
            the Entity doesn't need added to the PriorityQueue."""

        self._pqEntities._Add_Entity(entity)

        

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
