import os
import errno
import pdb
import sfml as sf
import config

#This will be a list of sfml.RenderStates, which contain the tile_Atlas textures


class Tile(object):
    """Denotes a single tile within a chunk."""
    def __init__( self ):
        self._is_Active = False    #Tells whether or not the tile is visible or not
        self._tileID = 0           #Identifies the type of tile that is drawn (denotes tile IDs on the tile_atlas.)
        self._is_Solid = False     #Tells if this tile is solid or not (is there no transparencies in the texture for the tileType.)

    def _Set_Is_Active( self ):
        """Automatically determines if the tile is active or not depending on the tile's type."""
        if self._tileID != 0:
            self._is_Active = True
        else:
            self._is_Active = False

    def __str__( self ):
        """This is the tile's string representation for when it is saved to a file."""
        offset = self._tileID%10    #This will get the first digit for our tileID

        return str((self._tileID-offset)/10) + str(offset)


class Chunk(object):
    """Denotes one of many chunks that are used within the game's world.
    The Chunks contain 16x16 Tiles at the moment..."""
    def __init__( self ):
        #Constructs our list of lists for the tiles within the chunk (3-dimensional, because of the layers.)
        #The background layer is represented by the 0th item in self._tiles. While the foreground layer represented by the len(self._tiles)-1 item in self._tiles
        #Access like so self._tiles[y][x][z]
        self._tiles = [ [ [ Tile() for k in range(config.CHUNK_LAYERS) ] for i in range(config.CHUNK_TILES_WIDE) ] for j in range(config.CHUNK_TILES_HIGH) ]

        #Initializes a storage container for vertex Arrays
        self._mesh = []

        #A mesh for each layer
        for i in xrange(config.CHUNK_LAYERS):
            self._mesh.append([])             #To draw with a tile atlas, where tile_atlas is of type sf.Texture, App.draw(v_array, tile_atlas)

        #The chunk position denotes the spot that the chunk's mesh will be drawn to inside the window
        self._world_Position = None      #This is a tuple, do not alter the elements of it!

        self._window_Position = None

        self._is_Loaded = False      #Tells whether or not there is any dat

        self._is_Empty = True

    def _Set_Tile_Type( self, x, y, z, tileType ):
        """This is for altering the tileType of a specific tile within this chunk."""

        self._tiles[y][x][z]._tileID = tileType
        self._tiles[y][x][z]._Set_Is_Active()

        #This assumes that our tileTypes are arranged in categories on the number line, thus hinting a type for a range of tile types  (solid/transparent.)
        if tileType > 0 and tileType <= 20:
            self._tiles[y][x][z]._is_Solid = True
        else:
            self._tiles[y][x][z]._is_Solid = False


    def _Load_Data( self ):
        """From the data within the chunk's file, we then give this list of lists as an argument for the Chunk's _Load_Data().
        So from here we'll update the self._tiles list of lists with a list of lists of similar size (the data.)"""

        fileName = config.Chunk_Directory + "/" + str(self._world_Position[0]) + " " + str(self._world_Position[1]) + ".txt"

        failureFlag = False

        try:
            fileObj = open(fileName, "r")

            dataBuffer = fileObj.read()

            offset = 0

            for row in xrange(config.CHUNK_TILES_HIGH):
                for col in xrange(config.CHUNK_TILES_WIDE):
                    for depth in xrange(config.CHUNK_LAYERS):

                        #The 1d index for the dataBuffer's current number
                        index = ((row*config.CHUNK_TILES_WIDE + col)*config.CHUNK_LAYERS + depth)*3 + offset    #Note that the *3 refers to the spaces taken up by each element in the data file.

                        self._Set_Tile_Type(col, row, depth, int(dataBuffer[index])*10 + int(dataBuffer[index+1]))
                        self._tiles[row][col][depth]._Set_Is_Active()  #This will not always set a tile to active (if tileType is 0, then it isn't active)

            #Flag that the chunk has been updated with data
            self._is_Loaded = True

            fileObj.close()

        except Exception:
            print fileName, "data file wasn't found, so the chunk will be filled in as though empty."

            #If the file doesn't exist, then we can just fill our chunk with transparent tiles!
            for row in xrange(config.CHUNK_TILES_HIGH):
                for col in xrange(config.CHUNK_TILES_WIDE):
                    for depth in xrange(config.CHUNK_LAYERS):

                        self._Set_Tile_Type(col, row, depth, 0)
                        #The constructor already sets the tile as inactive, so we won't bother with that.

    def _Unload( self ):
        """This is where we'll be saving the contents of a chunk to a file."""

        fileName = config.Chunk_Directory + "/" + str(self._world_Position[0]) + " " + str(self._world_Position[1]) + ".txt"

        #try:
        fileObj = open(fileName, "w")       #This won't provoke errors, because the file will either be created or overwritten.

        #The attributes and the tile IDs need to be assembled into a string representation and written to our fileObj

        dataString = ""

        for row in xrange(config.CHUNK_TILES_HIGH):
            for col in xrange(config.CHUNK_TILES_WIDE):
                for depth in xrange(config.CHUNK_LAYERS):

                    dataString += str(self._tiles[row][col][depth]) + " "     #This gets our TWO digits for the current tileID and adds a space onto the end of it

        fileObj.write(dataString)

        fileObj.close()     #Without this, there could be a corrupted file
        #except Exception:
            #print fileName, "failed to load, because it does not exist!"

    def _Flag_Update( self ):
        """This will determine if a chunk is empty or not depending on its meshes (a chunk with an empty mesh might as well be empty.)"""
        self._is_Empty = True

        for mesh in self._mesh:
            if len(mesh) != 0:
                self._is_Empty = False

    def _Build_Mesh( self ):
        """We create a mesh here using a VertexArray for a chunk that's on the screen. This only is meant to be for chunk's in relation to their position on the screen.
        Chunks off the screen don't need to have their meshes updated for no reason, but they can still have their data loaded before getting onto the screen."""
        #Makes sure that we have an empty vertex array to add to
        for mesh in self._mesh:
            del mesh[:]

        #Handles the building of the tiles within the chunk
        for j in xrange(config.VIEW_TILE_HEIGHT):
            for i in xrange(config.VIEW_TILE_WIDTH):
                #This assumes that depth 0 is the very front of the screen.
                for k in xrange(config.CHUNK_LAYERS):

                    if self._tiles[j][i][k]._is_Active:

                        self._Build_Tile(i, j, k, self._tiles[j][i][k]._tileID)

                        #If this tile isn't partially see-through, then all tiles behind it are occluded and we don't need to add them to their meshes.
                        if self._tiles[j][i][k]._is_Solid:
                            #This is confirmed to correctly break out of ONLY the CHUNK_LAYERS loop and still allow the other loops to continue.
                            break

    def _Build_Tile( self, x, y, layer, tileType ):
        """This is where we are adding a single tile in relation to its position within the chunk to our VertexArray _mesh."""
        #Calculates the position inside of our window where the tile will be placed
        tileXPos = (self._window_Position[0] * config.TILE_SIZE*config.CHUNK_TILES_WIDE)+(config.TILE_SIZE*x)
        tileYPos = (self._window_Position[1] * config.TILE_SIZE*config.CHUNK_TILES_HIGH)+(config.TILE_SIZE*y)

        #Determine the coordinates of the tileType for our tile atlas (TILE_ATLAS_SIZE^2 possible tileTypes) (not working with pixel coords yet)
        textXPos = (tileType-1) % config.TILE_ATLAS_SIZE
        textYPos = (tileType-1-textXPos) / config.TILE_ATLAS_SIZE

        #Normalize the texture positions!
        textXPos *= config.TILE_SIZE
        textYPos *= config.TILE_SIZE

        #Puts the four vertices inside of our vertex Array (represents a single tile quad.)
        self._mesh[layer].append(sf.Vertex( (tileXPos, tileYPos), sf.Color.WHITE, (textXPos, textYPos) ))
        self._mesh[layer].append(sf.Vertex( (tileXPos, tileYPos+config.TILE_SIZE), sf.Color.WHITE, (textXPos, textYPos+config.TILE_SIZE) ))
        self._mesh[layer].append(sf.Vertex( (tileXPos+config.TILE_SIZE, tileYPos+config.TILE_SIZE), sf.Color.WHITE, (textXPos+config.TILE_SIZE, textYPos+config.TILE_SIZE) ))
        self._mesh[layer].append(sf.Vertex( (tileXPos+config.TILE_SIZE, tileYPos), sf.Color.WHITE, (textXPos+config.TILE_SIZE, textYPos) ))

class Chunk_Manager(object):
    """Handles the chunks on the screen. Determines which chunks need their meshes updates, which chunks aren't empty.
    which chunks are on the screen, etc. And this will also be very important within the game state, as the game state will need to
    get tile data for the chunks within the window."""
    def __init__( self, chunkPosition, chunkInWindow ):
        #viewCoords is a tuple of integers containing the world chunk position for the top left chunk on the window
        self._x_World_Chunk_Position = chunkPosition[0]
        self._y_World_Chunk_Position = chunkPosition[1]

        self._chunks_In_Window_X = chunkInWindow[0]
        self._chunks_In_Window_Y = chunkInWindow[1]

        self._chunk_Dict = {}   #This stores all of the chunks (even outside of the wndow) around the area in the world the window's position is.

        #These will all contain chunk pointers to the _chunk_Dict's chunks that apply
        self._load_List = []
        self._rebuild_List = []
        self._unload_List = []
        self._flag_List = []
        self._render_List = []

        #This tells us whether or not a chunk's contents  have rebuilt or loaded
        self._force_Visibility_Update = False


        #Here we must add in the chunks that are visible to the screen into our chunk dictionary (along with our buffer of chunks outside of the screen.)
        for i in xrange( self._x_World_Chunk_Position-1, self._x_World_Chunk_Position + self._chunks_In_Window_X+1 ):
            for j in xrange( self._y_World_Chunk_Position-1, self._y_World_Chunk_Position + self._chunks_In_Window_Y+1 ):
                #This will initialize us a new chunk to use
                self._chunk_Dict[(i,j)] = Chunk()

                pChunk = self._chunk_Dict[(i,j)]    #This creates a pointer to our chunk in the chunk dictionary

                pChunk._window_Position = [ i - self._x_World_Chunk_Position, j - self._y_World_Chunk_Position ]    #This will set the chunk's position within the window (starting from the top-left.)

                pChunk._world_Position = (i,j)

                self._load_List.append(pChunk)      #Here we store our pointer in the load list, so that the chunk can have its data loaded

        self._tile_Atlas_List = []
        
        #This updates our global tile_Atlas_List variable to contain the textures for the tile atlases of each chunk layer
        for layer in xrange(config.CHUNK_LAYERS):
            try:
                self._tile_Atlas_List.append(sf.RenderStates(-1, None, sf.Texture.load_from_file('Resources/tileAtlas'+str(layer)+'.png'), None))
                
            except sf.PySFMLException:
                print "The tileAtlasX.png doesn't exist yet!\nConverting .jpg version to .png now!"
                
                oldImg = sf.Image.load_from_file('Resources/tileAtlas'+str(layer)+'.bmp')
      
                newImg = sf.Image.load_from_pixels(oldImg.width, oldImg.height, oldImg.get_pixels())

                newImg.create_mask_from_color(sf.Color(255,0,255), 0)

                print newImg[70,0]

                newImg.save_to_file('Resources/tileAtlas'+str(layer)+'.png')

                self._tile_Atlas_List.append(sf.RenderStates(-1, None, sf.Texture.load_from_file('Resources/tileAtlas'+str(layer)+'.png'), None))
        

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


    def _Render_Chunks( self, renderWindow ):
        """This renders the chunks that are within the render list."""

        #print self._render_List

        for pChunk in self._render_List:
            for layer in xrange(config.CHUNK_LAYERS-1, -1, -1):
                
                renderWindow.draw(pChunk._mesh[layer], sf.QUADS, self._tile_Atlas_List[layer])











