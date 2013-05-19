import sfml as sf
import components
import config

#Maybe we can include the Components file here and then have
#assemblage functions for creating common entities.

def Assemble_Text_Box(sEntityName, sEntityType, attribDict):
    """This assembles a box with text in it!"""
    entity = Entity(sEntityName, sEntityType, {})

    #The first argument represents the ID of the component with respect to its type (multiple components of a single type need to have different IDs.)
    entity._Add_Component(components.Text_Line({'componentID': attrib, 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height'], 'text': attribDict['text'], 'font': attribDict['Font'][0]}))
    entity._Add_Component(components.Box({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height']}))

    return entity

def Assemble_Button(sEntityName, sEntityType, attribDict):
    """This assembles a box with text in it! And sets up some other
    components that'll store important information we might need later."""
    entity = Entity(sEntityName, sEntityType, {})
    
    entity._Add_Component(components.Box({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height']}))
    entity._Add_Component(components.Text_Line({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height'], 'text': attribDict['text'], 'font': attribDict['Font'][0]}))
    entity._Add_Component(components.Flag({'componentID': '0', 'flag': False}))

    return entity

def Assemble_Player(sEntityName, sEntityType, attribDict):
    entity = Entity(sEntityName, sEntityType, {})

    entity._Add_Component(components.Animated_Sprite('0', iFrameWidth, iFrameHeight, {sAnimation: [texture for sAnimation, texture in dTextureStrips.items()]}))
    entity._Add_Component(components.Position('0', (0,0)))

    return entity

def Assemble_Chunk(sName, sType, attribDict):
    entity = Entity(sEntityName, sEntityType, {})

    entity._Add_Component(components.Mesh())

    entity._Add_Component(components.Position(attribDict['WindowPos'].split(',')))
    entity._Add_Component(components.Position(attribDict['WorldPos'].split(',')))

    entity._Add_Component(components.Flag("Is Empty", True))
    entity._Add_Component(components.Flag("Is Loaded", False))    

    #Here a list comprehension is used to construct a list of lists of lists of Tile components.
    entity._Add_Component([[[components.Tile() for depth in xrange(config.CHUNK_LAYERS)]   \
                             for col in xrange(config.CHUNK_TILES_WIDE)]                    \
                            for row in xrange(config.CHUNK_TILES_HIGH)])

    return entity


class Entity(object):
    def __init__(self, sEntityName, sEntityType, dComponents):
        #The id is mostly for debugging purposes.
        self._sName = sEntityName
        self._sType = sEntityType

        #componentName:component
        self._dComponents = {}        #Drawable components that are in the dComponents dictionary will have a pointer to them in this list.
        self._lDrawables = []

        #Updatable components that hold pointer variables that point to the updatable components in the dComponents dictionary.
        self._lUpdatables = []

        self._bExpired = False

        for key in dComponents.keys():
            self._Add_Component(dComponents.pop(key))

        #What if there was to be different types of components
        #Then we could have all self-contained drawable components draw one way
        #And all RenderState dependent drawable components drawn another way.
        #And we could also have sound components that will all be played at certain times.

    def _Add_Component(self, componentInstance):
        """This takes in an instance of a class that inherits from the Component class
        and then it adds that instance into the list of components for this particular entity."""
        self._dComponents[componentInstance._Get_Name()] = componentInstance

        #These if statements will save a pointer of the same variable as in dComponents if True.

        if componentInstance._Get_Updatable():
            self._lUpdatables.append(componentInstance)

        if componentInstance._Get_Drawable():
            self._lDrawables.append(componentInstance)

    def _Remove_Component(self, sCompName):
        """This searches through our list of components for the component with
        the specified ID and then removes it from the list."""
        del self._dComponents[sCompName]

    def __len__(self):
        return len(self._dComponents)

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
        for i in xrange(len(self._lDrawables)):

            #This calls the Drawable component's _Render() method.
            self._lDrawables[i]._Render(renderWindow)

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



        

class Entity_List(Entity):
    """Like the name says, this will store Entities. And it will update/render those entities accordingly."""
    def __init__(self, sName):
        Entity.__init__(self, sName, sType)

        self._lEntities = []

    def _Add_Entity(self, Entity):
        """This allows system functions to be able to add in new entities into the game (during a state.)
        (This could be used for when the player enters a new chunk (that has enemies in it.))"""
        self._lEntities.append(Entity)

    def _Remove_Entity(self, sEntityName):
        """This will allow system functions to remove entities from the entity list.
        (They could have been moved off of the screen?)"""
        for i in xrange(len(self._lEntities)):
            if self._lEntities[i]._Get_Name() == sEntitiyName:
                self._lEntities.pop(i)
                break

    def _Get_Entity(self, sEntityName):
        """This will allow system functions to get a specific entitiy from the list."""
        for i in xrange(len(self._lEntities)):
            if self._lEntities[i]._Get_Name() == sEntitiyName:
                return self._lEntities[i]

    def _Update(self, timeElapsed):
        """This will be where we update all of the contained entities. (This happens once per game update!)"""
        for indx in xrange(len(self._lEntities)):
            #This will check to see if the current Entity has signaled to be removed.
            if self._lEntities[indx]._Is_Expired():
                #So we let the entity do its cleaning up, then we remove it from the Entity_List entirely.
                self._lEntities[indx]._On_Expire()
                self._Remove_Entity(self._lEntities[indx]._Get_Name())
                #We won't need to update a removed entity!
                break

            #Now since that this entity hasn't been removed, we'll update it.
            self._lEntities._Update(timeElapsed)

    def _Render(self, renderWindow):
        """Here we render the contained entities onto the screen. (This happens once per program loop!)"""
        for indx in xrange(len(self._lEntities)):
            self._lEntities._Render(renderWindow)

class Chunk_Manager(Entity):
    """Handles the chunks on the screen. Determines which chunks need their meshes updates, which chunks aren't empty.
    which chunks are on the screen, etc. And this will also be very important within the game state, as the game state will need to
    get tile data for the chunks within the window."""
    def __init__( self, sName, sType, attribDict):
        Entity.__init__(self, sName, sType)
        #viewCoords is a tuple of integers containing the world chunk position for the top left chunk on the window
        self._Add_Component(components.Position('ChunkPosition', attribDict['ChunkPosition']))

        self._Add_Component(components.Position('ChunkPosition', attribDict['ChunksInWindow']))

        config.CHUNK_LAYERS = attribDict['ChunkLayers']

        self._Add_Component(components.List('TileAtlas'))

        for i in xrange(config.CHUNK_LAYERS):
            self._Get_Component('TileAtlas')._Add_To_List(attribDict['TileAtlas'+str(i)])

        #These will all contain chunk pointers to the _chunk_Dict's chunks that apply
        self._load_List = []
        self._rebuild_List = []
        self._unload_List = []
        self._flag_List = []
        self._render_List = []

        #This tells us whether or not a chunk's contents  have rebuilt or loaded
        self._force_Visibility_Update = False

        #This will strictly assemble the chunks around the outside of the chunks on the screen (the first items in the loadList get loaded last, so we add these first!)

        #This only will loop through the chunks to the left and right of the screen.
        for i in xrange( self._Get_Component('ChunkPosition')._Get_X()-1, self._Get_Component('ChunkPosition')._Get_X() + self._Get_Component('ChunksInWindow')._Get_X()+1 ):
            for j in xrange( self._Get_Component('ChunkPosition')._Get_Y()-1, self._Get_Component('ChunkPosition')._Get_Y() + self._Get_Component('ChunksInWindow')._Get_Y()+1, self._Get_Component('ChunksInWindow')._Get_Y()+1 ):

                self._Add_Component(Assemble_Chunk(str(i)+','+str(j),'Chunk', {'WindowPos': [ i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position ], 'WorldPos': (i,j)}))

                pChunk = self._Get_Component(str(i)+','+str(j))
                
                loadList.append(pChunk)

        #This does the same thing as the previous loop, but with different chunks (above the screen and below the screen.)
        for i in xrange( self._Get_Component('ChunkPosition')._Get_X()-1, self._Get_Component('ChunkPosition')._Get_X() + self._Get_Component('ChunksInWindow')._Get_X()+1, self._Get_Component('ChunksInWindow')._Get_X()+1 ):
            for j in xrange( self._Get_Component('ChunkPosition')._Get_Y()-1, self._Get_Component('ChunkPosition')._Get_Y() + self._Get_Component('ChunksInWindow')._Get_Y()+1):

                print (i,j)

                self._Add_Component(Assemble_Chunk(str(i)+','+str(j),'Chunk', {'WindowPos': [ i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position ], 'WorldPos': (i,j)}))

                pChunk = self._Get_Component(str(i)+','+str(j))
                
                loadList.append(pChunk)

        #This will assemble the chunks that are inside of the screen (these chunks need loaded first and their meshes built.)
        for i in xrange( self._Get_Component('ChunkPosition')._Get_X(),  self._Get_Component('ChunkPosition')._Get_X() + self._Get_Component('ChunksInWindow')._Get_X()):
            for j in xrange( self._Get_Component('ChunkPosition')._Get_Y(),  self._Get_Component('ChunkPosition')._Get_Y() + self._Get_Component('ChunksInWindow')._Get_Y()):
                
                self._Add_Component(Assemble_Chunk(str(i)+','+str(j),'Chunk', {'WindowPos': [ i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position ], 'WorldPos': (i,j)}))

                pChunk = self._Get_Component(str(i)+','+str(j))
                
                loadList.append(pChunk)
                rebuildList.append(pChunk)

    def _Update( self ):
        """This handles the updating of the chunks and will be done each main loop through the program (which will likely be more often than the game ticks or in some cases the same.)"""

        self._Update_Load_List()

        self._Update_Rebuild_List()

        self._Update_Unload_List()

        if self._force_Visibility_Update:
            self._Update_Flag_List()

            #Update the render list if the camera's Position has changed
            self._Update_Render_List()

            self._force_Visibility_Update = False

    def _Get_Tile_IDs(self, listOfTiles):
        """The listOfTiles will just be a list of tuples containing
        the coordinates of the tiles that are being queried for tile IDs."""

        tileIDs = []

        #This assumes we take a list of tuples as an argument.
        for (x, y, z) in listOfTiles:

            #Fill the variables we're going to be using to find the tile and chunk we're altering.
            xTileOffset = x % config.CHUNK_TILES_WIDE                                                           #This represents the tile position within the chunk it belongs to
            xChunkOffset = int((x-xTileOffset) / config.CHUNK_TILES_WIDE) + self._x_World_Chunk_Position        #This represents the chunk position (of the chunk the tile is inside of) within the window!

            yTileOffset = y %config.CHUNK_TILES_HIGH
            yChunkOffset = int((y-yTileOffset) / config.CHUNK_TILES_HIGH) + self._y_World_Chunk_Position

            tileIDs.append(self._chunk_Dict[(xChunkOffset, yChunkOffset)]._Get_Tile_Type(xTileOffset, yTileOffset, z))

        return tileIDs

    def _Alter_Tiles( self, listOfTiles ):
        """This method will be what alters the tiles inside of our model.
        But the tile locations that are entered will only be in relation to the chunks/tiles on the window."""

        #Just initializing some variables for the upcoming for loop
        xTileOffset = 0
        xChunkOffset = 0
        yTileOffset = 0
        yChunkOffset = 0

        alteredChunks = {}

        #This assumes all elements of listOfTiles are tuples with four integers in each.
        for (x, y, z, newTileType) in listOfTiles:

            #Fill the variables we're going to be using to find the tile and chunk we're altering.
            xTileOffset = x % config.CHUNK_TILES_WIDE                                                           #This represents the tile position within the chunk it belongs to
            xChunkOffset = int((x-xTileOffset) / config.CHUNK_TILES_WIDE) + self._x_World_Chunk_Position        #This represents the chunk position (of the chunk the tile is inside of) within the window!

            yTileOffset = y %config.CHUNK_TILES_HIGH
            yChunkOffset = int((y-yTileOffset) / config.CHUNK_TILES_HIGH) + self._y_World_Chunk_Position

            #Now we're altering the chunk at chunk position ( self._x_World_Chunk_Position + xChunkOffset, self._y_World_Chunk_Position + yChunkOffset )
            self._chunk_Dict[(xChunkOffset, yChunkOffset)]._Set_Tile_Type(xTileOffset, yTileOffset, z, newTileType)

            alteredChunks[(xChunkOffset, yChunkOffset)] = 1

        for chunkPosition in alteredChunks.keys():
            self._rebuild_List.append(self._chunk_Dict[chunkPosition])

    def _Move_Chunk_Position( self, xOffset, yOffset ):
        """This will add/remove chunks from our dictionary and is meant to be used when we translate our window across the chunk world (because scrolling.)
        There are chunks assumed to already be active on the screen."""
        #If the chunk position hasn't been moved, then we don't need to rebuild any meshes or initialize any new chunks
        if xOffset != 0 or yOffset != 0:

            #Here we update our world chunk coords.
            self._x_World_Chunk_Position += xOffset
            self._y_World_Chunk_Position += yOffset


            #These variables are determined before the following for loop because they will otherwise have to be calculated more than once.
            if (self._chunks_In_Window_X + xOffset) % 2 == 0:
                xEven = True
            else:
                xEven = False

            if (self._chunks_In_Window_Y + yOffset) % 2 == 0:
                yEven = True
            else:
                yEven = False

            #print self._chunk_Dict

            #If we move our world chunk position, then we will essentially need to reset all of the chunk's window positions (that are still on the screen.)
            #And the chunks that move off the screen will remain unaltered in case they return to their original window position (which then it won't need its mesh rebuilt.)
            for i in xrange( self._x_World_Chunk_Position - 1, self._x_World_Chunk_Position + self._chunks_In_Window_X + 1 ):
                for j in xrange( self._y_World_Chunk_Position - 1, self._y_World_Chunk_Position + self._chunks_In_Window_Y + 1 ):


                    #print i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position

                    #This checks to see if the chunk already exists in our dictionary (it was already inside the window or window buffer.)
                    if self._chunk_Dict.get((i,j), None) != None:

                        pChunk = self._chunk_Dict[(i,j)]

                        #print "Current window position:", pChunk._window_Position[0], pChunk._window_Position[1]
                        #print "Current world position:", pChunk._world_Position[0], pChunk._world_Position[1]

                        #Each chunk needs to be checked to see if its position isn't equal to what we'll be setting it to.
                        #So then the chunks that have the correct position already won't be added to the rebuild list (their mesh is already correct.)
                        if pChunk._window_Position != [i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position]:


                            #print "Changing the window position", pChunk._window_Position[0], pChunk._window_Position[1]

                            #Then we need to update the window chunk position
                            pChunk._window_Position = [ i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position ]

                            #print pChunk._window_Position[0], pChunk._window_Position[1]

                            #and push the chunk onto the rebuild list
                            self._rebuild_List.append(pChunk)

                        #else:

                            #print "Not changing window position", pChunk._window_Position[0], pChunk._window_Position[1]


                    #If the chunk has yet to be initialized.
                    else:

                        #For each chunk that is initialized, there will be one that we will have to free from memory.

                        #Initialize a new chunk at position i,j in the world of chunks and put it into our dictionary.
                        self._chunk_Dict[(i,j)] = Chunk()

                        pChunk = self._chunk_Dict[(i,j)]

                        #Set the chunk's screen and world positions.
                        pChunk._world_Position = (i,j)

                        pChunk._window_Position = [ i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position ]

                        #print "new chunk at", i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position

                        self._load_List.append(pChunk)
                        #Schedule an old chunk to be unloaded and then removed from the chunk dictionary

                        #Find the middle chunk position inbetween the previous and the next world chunk position.
                        midChunkX = self._x_World_Chunk_Position - xOffset + (self._chunks_In_Window_X + xOffset)/2   #Note that the division operator will round down when the result isn't a whole number.
                        midChunkY = self._y_World_Chunk_Position - yOffset + (self._chunks_In_Window_Y + yOffset)/2

                        #These if statements make it possible to use this method when there are an even or odd amount of chunks in the window (it'll be one or the other.)
                        if xEven:
                            p = midChunkX - (i - midChunkX) - 1
                        else:
                            p = midChunkX - (i - midChunkX)

                        if yEven:
                            q = midChunkY - (j - midChunkY) - 1
                        else:
                            q = midChunkY - (j - midChunkY)

                        #print "chunk removed at", p, q

                        #This saves the chunk's data
                        pChunk = self._chunk_Dict.get((p,q), None)

                        if pChunk != None:
                            self._unload_List.append(pChunk)

    def _Update_Load_List( self ):
        """This will signal chunks to load its data from their text files. Don't confuse this for updating the meshes of the chunks."""
        iNumberOfChunksLoaded = 0

        for iChunk in xrange(len(self._load_List)-1, -1, -1):

            #Checks to see if the chunk has been loaded yet
            if self._load_List[iChunk]._is_Loaded == False:

                #This limits chunk loading for a single tick
                if iNumberOfChunksLoaded != 3:

                    #Loads the tile data from its file
                    self._load_List[iChunk]._Load_Data()
                    self._load_List[iChunk]._is_Loaded = True

                    #print "Signaling to rebuild a CHUNK MESH!"
                    self._rebuild_List.append(self._load_List.pop(iChunk))

                    iNumberOfChunksLoaded += 1

                    self._force_Visibility_Update = True

    def _Update_Rebuild_List( self ):
        """If a chunk has been updated and added to the rebuild_List. Then we will be signaling it to rebuild its mesh here. I also took out the section that
        was trying to optimize the render calls. But then I realized that in a 2d world, chunks can't really be occluded by other chunks (was thinking in 3d.)"""
        iNumberOfChunksRebuilt = 0
        for iChunk in xrange(len(self._rebuild_List)-1, -1, -1):

            #Checking to see if the chunk has been loaded yet
            if self._rebuild_List[iChunk]._is_Loaded:

                #This limits our chunk rebuilds to 3
                if iNumberOfChunksRebuilt != 3:
                    #print "Building a mesh..."
                    self._rebuild_List[iChunk]._Build_Mesh()

                    self._flag_List.append(self._rebuild_List.pop(iChunk))  #removes the chunk pointer from the list

                    iNumberOfChunksRebuilt += 1

                    self._force_Visibility_Update = True

    def _Update_Unload_List( self ):
        """Here we will be freeing the memory associated with chunks that are far enough away from the window that we don't care about them anymore.
        So we will pop them from the _chunk_Dict and then save their data to their respective file."""
        #The del command will probably be helpful here
        iNumberOfChunksUnloaded = 0
        for iChunk in xrange(len(self._unload_List)-1, -1, -1):
            if iNumberOfChunksUnloaded < 3 and self._unload_List[iChunk]._is_Loaded:

                self._unload_List[iChunk]._Unload()    #This will save the contents of our chunk to a file (so we can free our memory.)

                #Now we take the chunk and chunk pointer variables outside of the lists because they aren't needed anymore.
                self._chunk_Dict.pop((self._unload_List[iChunk]._world_Position[0], self._unload_List[iChunk]._world_Position[1]))

                del self._unload_List[iChunk]

                iNumberOfChunksUnloaded += 1

    def _Update_Flag_List( self ):
        """The chunks within the flag list have just recently either been loaded or had their tile data altered. So here we will see if those chunks are empty. And if they are,
        we'll just update their flags."""

        #This computation is quite small, so I haven't limited the updates.
        for iChunk in xrange(len(self._flag_List)-1, -1, -1):
            #This will tell the chunk to determine if it is empty or not
            self._flag_List[iChunk]._Flag_Update()

            #print "updating flagList!"

            del self._flag_List[iChunk]     #This removes the pointer from our flag update list.

    def _Update_Render_List( self ):
        """Depending on where window is in the world and which chunks are renderable. We will determine which chunks are going to be rendered
        next time rendering occurs."""

        del self._render_List[:]

        #Only the chunks within the window are applicable
        #This will iterate through all of the chunks inside the window at the moment.
        for i in xrange( self._x_World_Chunk_Position, self._x_World_Chunk_Position + self._chunks_In_Window_X):
            for j in xrange(self._y_World_Chunk_Position, self._y_World_Chunk_Position + self._chunks_In_Window_Y ):

                #Check to see if the chunk is loaded and not empty!
                if self._chunk_Dict[(i,j)]._is_Loaded and not self._chunk_Dict[(i,j)]._is_Empty:

                    #print "A chunk is being added to the render List!"

                    self._render_List.append(self._chunk_Dict[(i,j)])   #Put the chunk pointer into the render list!


    def _Render( self, renderWindow ):
        """This renders the chunks that are within the render list."""

        #print self._render_List

        for pChunk in self._render_List:
            for layer in xrange(config.CHUNK_LAYERS-1, -1, -1):
                
                renderWindow.draw(pChunk._mesh[layer], sf.QUADS, self._tile_Atlas_List[layer])

