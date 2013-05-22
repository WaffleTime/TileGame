import os
import sfml as sf
import xml.etree.ElementTree as ET
import config
import entities

#####################################################################
#--SS-Y--Y--SS-TTTTTT-EEEEE-M---M---SS------------------------------#
#-S----YY--S-----T----E-----MM-MM--S--------------------------------#
#--S---Y----S----T----EE---M--M-M---S-------------------------------#
#SS----Y--SS-----T----EEEE-M----M-SS--------------------------------#
#####################################################################

class System_Manager(object):

    lActionSystems = []
    lStateSystems = []

    @staticmethod
    def _Empty_Systems():
        """This simply will empty the Systems that were signaled to be called."""
        del System_Manager.lActionSystems[:]
        del System_Manager.lStateSystems[:]

    @staticmethod
    def _Add_System(sType, sSystemFuncName, lEntities):
        """This will be for adding in various types of systems into the game. Systems will exist as more than just a single function.
        For the different types of systems, I'd like them to be handled differently. A state system for instance will have two functions associated with it.
        One function will be to activate continuously and the other one will activate once when the system is removed."""

        if sType == 'action':
            System_Manager.lActionSystems.append((sSystemFuncName, lEntities))

        elif sType == 'state':
            System_Manager.lStateSystems.append((sSystemFuncName, lEntities))

    @staticmethod
    def _Remove_State_System(sSystemFuncName):
        """This will be for removing the systems that stay active until told otherwise (this is where we say otherwise.)
        Since the Actions systems will be removed once they are executed, they don't really play an importance here."""

        for indx in xrange(len(System_Manager.lActionSystems)-1,-1,-1):
            if System_Manager.lActionSystems[indx][0] == sSystemFuncName:
                System_Manager.lActionSystems.pop(indx)
                break
        for indx in xrange(len(System_Manager.lStateSystems)-1,-1,-1):
           if System_Manager.lStateSystems[indx][0] == sSystemFuncName:
                System_Manager.lStateSystems.pop(indx)
                break

    @staticmethod
    def _Get_Active_Systems():
        """This will return the active systems. Removing the actions from there containers, while just getting copies of the states."""
        lSystems = System_Manager.lActionSystems + System_Manager.lStateSystems

        del System_Manager.lActionSystems[:]

        return lSystems

def Move_Player_Right(dEntities):
    """This will move the player to the right and checking to see if a chunk border was crossed.
    If the chunk border was crossed, then we'd have to signal for the Chunk_Manager and Inhabitant_Manager
    to be added/removed to/from (the Inhabitant_Manager doesn't need things removed necessarily though, so only additional inhabitants will appear.)"""

    #Do a Chipmunk impulse on the colliding shape thingy (the Entity will update the actual position on its own.)
    pass

    #Check to see if the player's chunk position is different than the one at the player's coords (chipmunk coords.)

        #If it is, then we can signal the System function to execute a function that loads/removes in Chunk entities for the Chunk_Manager and loads in Inhabitant entities for the Inhabitant_Manager.


def Move_Player_Left(dEntities):
    """This will move the player to the left and checking to see if a chunk border was crossed.
    If the chunk border was crossed, then we'd have to signal for the Chunk_Manager and Inhabitant_Manager
    to be added/removed to/from (the Inhabitant_Manager doesn't need things removed necessarily though, so only additional inhabitants will appear.)"""

    #Do a Chipmunk impulse on the colliding shape thingy (the Entity will update the actual position on its own.)

    pass
    #Check to see if the player's chunk position is different than the one at the player's coords (chipmunk coords.)

        #If it is, then we can signal the System function to execute a function that loads/removes in Chunk entities for the Chunk_Manager and loads in Inhabitant entities for the Inhabitant_Manager.

def New_Save(dEntities):
    """This will setup a new saved game directory along with the player's
    xml data. Along with this system there should be other functions
    that will move the chunk data into this directory and also
    fetch the entity xml data for the beginning level."""

    #Create a new saved game directory (non-optional directory name, whatever isn't already taken.)
    #Directory will be added to config.Game_Directory + "\\SavedGames"
    os.chdir(config.Game_Directory + "\\SavedGames")
    
    lyst = os.listdir(os.getcwd())

    counter = 0
    
    #Iterate through the lyst counting the saved games.
    for i in lyst:
        #Checks if the current item
        #   is a Saved Game dir.
        if (i[0:3] == "Save"):
            counter += 1

    #This is so that the counter is one more than the total
    #   amount of saves.
    counter += 1

    #This is the new saved game's folder
    os.mkdir(os.getcwd() + "\\Save" + str(counter))

    os.chdir(os.getcwd() + "\\Save" + str(counter))

    #Returns an ELement object that can be modified and
    #   and saved as an xml file. This will be the player's
    #   saved data.
    playerStats = ET.Element("Player Stats")

    #This adds an attribute
    playerStats.set("name", "Fagot point1")

    playerStats.append(ET.Element("Class", {"sub-class":"Fucker"}))
    playerStats.find("Class").text = "Hero"

    playerStats.append(ET.Element("CurHp"))
    playerStats.find("CurHp").text = 20
    playerStats.append(ET.Element("MaxHp"))
    playerStats.find("MaxHp").text = 20
    
    playerStats.append(ET.Element("CurMp"))
    playerStats.find("CurMp").text = 20
    playerStats.append(ET.Element("MaxMp"))
    playerStats.find("MaxMp").text = 20

    playerStats.append(ET.Element("Strength"))
    playerStats.find("Strength").text = 10
    playerStats.append(ET.Element("Intelligence"))
    playerStats.find("Intelligence").text = 10
    playerStats.append(ET.Element("Dexterity"))
    playerStats.find("Dexterity").text = 10
    playerStats.append(ET.Element("Agility"))
    playerStats.find("Agility").text = 10

    #This should save the xml we just created
    #   into the new saved directory
    ET.ElementTree(playerStats).write("Save" + str(counter))
    
    #Select this new saved game.
    config.Saved_Game_Directory = os.getcwd() + "\\Save" + str(counter)

def Load_Level_Data(dEntities):
    """This will be for copying chunk and entity data about a certain level into the current saved game's directory."""

    pass

def Load_Chunk_Entities(dEntities):
    """This will load in some Entities for the Chunk_"""
    pass
    
def Change_State(dEntities):
    """This will be able to be used by Inputs of various kinds as well as any other place in the Entity_Managers (or the other systems, but I don't want much of it.)
    It's objective is to make the Entity_Manager._Input_Update() method return a new lNextState variable for the main. And this variable will be able to change the state of the
    game to any other state!"""
    print dEntities['state']._Get_Component('STATE:0')._Get_State()
    #This will access the entity that is connected to the 'state' key and we then get the State component from it and call its _Get_State() method to get a string containing the two states (1st and 2nd level) for the next state to be.
    return dEntities['state']._Get_Component('STATE:0')._Get_State()       #The split breaks a string into chunks in-between a given character and puts those chunks into a list (which is what we want to return.)

def Oscillate_Box_Colors(dEntities):

    dEntities['box']._Get_Component('BOX:0')._Switch_Color()

    #This basically just tells EntityManager._Input_Update() that
    #   a state change isn't happening.
    return "NULL,NULL"







def Alter_Tiles(lTileData, ManChunkEntity):

    #Just initializing some variables for the upcoming for loop
    xTileOffset = 0
    xChunkOffset = 0
    yTileOffset = 0
    yChunkOffset = 0

    alteredChunks = {}

    chunkDict = ManChunkEntity._Get_Component(CHUNK_DICT)[(xChunkOffset, yChunkOffset)]
    worldPos = ManChunkEntity._Get_Component(WORLD_POS)._Get_Position()
    rebuildList = ManChunkEntity._Get_Component(REBUILD_LIST)

    #This assumes all elements of listOfTiles are tuples with four integers in each.
    for (x, y, z, newTileType) in lTileData:

        #Fill the variables we're going to be using to find the tile and chunk we're altering.
        #This represents the tile position within the chunk it belongs to
        xTileOffset = x % config.CHUNK_TILES_WIDE
        #This represents the chunk position (of the chunk the tile is inside of) within the window!
        xChunkOffset = int((x-xTileOffset) / config.CHUNK_TILES_WIDE) + worldPos[0]        

        yTileOffset = y %config.CHUNK_TILES_HIGH
        yChunkOffset = int((y-yTileOffset) / config.CHUNK_TILES_HIGH) + worldPos[1]

        #Now we're altering the chunk at chunk position ( self._x_World_Chunk_Position + xChunkOffset, self._y_World_Chunk_Position + yChunkOffset )
        chunkDict[(xChunkOffset, yChunkOffset)]._Get_Component(TILES)[xTileOffset][yTileOffset][z]._Set_Tile_ID(newTileType)

        alteredChunks[(xChunkOffset, yChunkOffset)] = 1

    for chunkPosition in alteredChunks.keys():
        rebuildList.append(chunkDict[chunkPosition])



def Move_Chunk_Position(dEntities):
    """This will add/remove chunks from our dictionary and is meant to be used when we translate our window across the chunk world (because scrolling.)
    There are chunks assumed to already be active on the screen."""
    #If the chunk position hasn't been moved, then we don't need to rebuild any meshes or initialize any new chunks
    if xOffset != 0 or yOffset != 0:

        #Here we update our world chunk coords.
        dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Add_To_X(xOffset)
        dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Add_To_Y(yOffset)

        worldPos = dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_Position()
        chunksInWindow = dEntities["ChunkMan"]._Get_Component("POS:ChunksInWind")._Get_Position()

        chunkDict = dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict")
        
        loadList = dEntities["ChunkMan"]._Get_Component("LIST:LoadList")
        rebuildList = dEntities["ChunkMan"]._Get_Component("LIST:RebuildList")
        unloadList = dEntities["ChunkMan"]._Get_Component("LIST:UnloadList")

        #These variables are determined before the following for loop because they will otherwise have to be calculated more than once.
        if (chunksInWindow[0] + xOffset) % 2 == 0:
            xEven = True
        else:
            xEven = False

        if (chunksInWindow[1] + yOffset) % 2 == 0:
            yEven = True
        else:
            yEven = False

        #If we move our world chunk position, then we will essentially need to reset all of the chunk's window positions (that are still on the screen.)
        #And the chunks that move off the screen will remain unaltered in case they return to their original window position (which then it won't need its mesh rebuilt.)
        for i in xrange( worldPos[0] - 1, worldPos[0] + chunksInWindow[0] + 1 ):
            for j in xrange( worldPos[1] - 1, worldPos[1] + chunksInWindow[1] + 1 ):

                #This checks to see if the chunk already exists in our dictionary (it was already inside the window or window buffer.)
                if chunkDict._Get(i+","+j) != None:

                    pChunk = chunkDict[i+","+j]

                    #Each chunk needs to be checked to see if its position isn't equal to what we'll be setting it to.
                    #So then the chunks that have the correct position already won't be added to the rebuild list (their mesh is already correct.)
                    if pChunk._Get_Component("POS:WindowPos")._Get_Position() != [i - worldPos[0], j - worldPos[1]]:

                        #Then we need to update the window chunk position
                        pChunk._Get_Component("POS:WindowPos")._Set_Position([ i - worldPos[0], j - worldPos[1] ])

                        #and push the chunk onto the rebuild list
                        rebuildList._Add(pChunk)

                    #else:

                        #print "Not changing window position", pChunk._window_Position[0], pChunk._window_Position[1]


                #If the chunk has yet to be initialized.
                else:

                    #For each chunk that is initialized, there will be one that we will have to free from memory.

                    #Initialize a new chunk at position i,j in the world of chunks and put it into our dictionary.
                    chunkDict[i+","+j] = entities.Assemble_Chunk( "%d, %d" % (i,j),     \
                                                                   "Chunk",              \
                                                                   {"WorldPos":i+","+j,
                                                                    "WindowPos":str(i - worldPos[0])+","+str(j - worldPos[1])} )

                    pChunk = chunkDict[i+","+j]

                    loadList._Add(pChunk)
                    #Schedule an old chunk to be unloaded and then removed from the chunk dictionary

                    #Find the middle chunk position inbetween the previous and the next world chunk position.
                    midChunkX = worldPos[0] - xOffset + (chunksInWindow[0] + xOffset)/2   #Note that the division operator will round down when the result isn't a whole number.
                    midChunkY = worldPos[1] - yOffset + (chunksInWindow[1] + yOffset)/2

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
                    pChunk = chunkDict[p+","+q]

                    unloadList._Add(pChunk)

def Update(dEntities):
    """This will initiate all of the different updates that need done for
    the Chunk Manager Entity."""
    
    Update_Load_List({"LoadList":dEntities["ChunkMan"]._Get_Component("LIST:LoadList")})

    Update_Rebuild_List({"RebuildList":dEntities["ChunkMan"]._Get_Component("LIST:RebuildList"),    \
                        "FlagList":dEntities["ChunkMan"]._Get_Component("LIST:FlagList"),           \
                        "VisibilityUpdate":dEntities["ChunkMan"]._Get_Component("FLAG:VisibilityUpdate")})

    Update_Unload_List({"UnloadList":dEntities["ChunkMan"]._Get_Component("LIST:UnloadList"),     \
                       "ChunkDict":dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict")})

    if dEntities["ChunkMan"]._Get_Component("FLAG:VisibilityUpdate")._Get_Flag():

        Update_Flag_List({"FlagList":dEntities["ChunkMan"]._Get_Component("LIST:FlagList")})

        #Update the render list if the camera's Position has changed
        Update_Render_List({"ChunkDict":dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict"),
                           "WorldPos":dEntities["ChunkMan"]._Get_Component("POS:WorldPos"),
                           "ChunksInWind":dEntities["ChunkMan"]._Get_Component("POS:ChunksInWind"),
                           "RenderList":dEntities["ChunkMan"]._Get_Component("RLIST:RenderList")})

        dEntities["ChunkMan"]._Get_Component("FLAG:VisibilityUpdate")._Set_Flag(False)



def Update_Load_List(dEntities):
    """This will signal chunks to load its data from their text files. Don't confuse this for updating the meshes of the chunks."""
    iNumberOfChunksLoaded = 0

    for iChunk in xrange(len(dEntities["LoadList"])-1,-1,-1):

        #Checks to see if the chunk has been loaded yet
        if dEntities["LoadList"][iChunk]._Get_Component("FLAG:IsLoaded")._Get_Flag() == False:

            #This limits chunk loading for a single tick
            if iNumberOfChunksLoaded != 4:

                #Loads the tile data from its file
                Load_Data({"chunk":dEntities["LoadList"][iChunk]})
                dEntities["LoadList"][iChunk]._Get_Component("FLAG:IsLoaded")._Set_Flag(True)

                dEntities["LoadList"]._Remove(iChunk)

                iNumberOfChunksLoaded += 1

            else:
                break

def Update_Rebuild_List(dEntities):
    """If a chunk has been updated and added to the rebuild_List. Then we will be signaling it to rebuild its mesh here. I also took out the section that
    was trying to optimize the render calls. But then I realized that in a 2d world, chunks can't really be occluded by other chunks (was thinking in 3d.)"""
    iNumberOfChunksRebuilt = 0
    for iChunk in xrange(len(dEntities["RebuildList"])-1,-1,-1):

        #Checking to see if the chunk has been loaded yet
        if dEntities["RebuildList"][iChunk]._Get_Component("FLAG:IsLoaded")._Get_Flag():

            #This limits our chunk rebuilds to 3
            if iNumberOfChunksRebuilt != 4:
                print "Building a mesh..."
                Build_Meshes({"chunk":dEntities["RebuildList"][iChunk]})

                iNumberOfChunksRebuilt += 1

                #This limits us to doing only one update to this component
                if iNumberOfChunksRebuilt == 1:

                    dEntities["VisibilityUpdate"]._Set_Flag(True)

                dEntities["FlagList"]._Add(dEntities["RebuildList"]._Pop(iChunk))  #removes the chunk pointer from the list

            else:
                break

def Update_Unload_List(dEntities):
    """Here we will be freeing the memory associated with chunks that are far enough away from the window that we don't care about them anymore.
    So we will pop them from the _chunk_Dict and then save their data to their respective file."""
    #The del command will probably be helpful here
    iNumberOfChunksUnloaded = 0
    for iChunk in xrange(len(dEntities["UnloadList"])-1,-1,-1):

        if iNumberOfChunksUnloaded < 3  \
           and dEntities["UnloadList"][iChunk]._Get_Component("FLAG:IsLoaded")._Get_Flag():

            Unload(dEntities["UnloadList"][iChunk])    #This will save the contents of our chunk to a file (so we can free our memory.)

            #print dEntities["UnloadList"]._Get(iChunk)._Get_Component(CWORLD_POS)._Get_Position()

            #Now we take the chunk and chunk pointer variables outside of the lists because they aren't needed anymore.
            chunkDict.pop(str(dEntities["UnloadList"][iChunk]._Get_Component("POS:WorldPos")._Get_X())  \
                          + "," + str(dEntities["UnloadList"][iChunk]._Get_Component("POS:WorldPos")._Get_Y()))

            dEntities["UnloadList"]._Remove(iChunk)

            iNumberOfChunksUnloaded += 1

def Update_Flag_List(dEntities):
    """The chunks within the flag list have just recently either been loaded or had their tile data altered. So here we will see if those chunks are empty. And if they are,
    we'll just update their flags."""

    #This computation is quite small, so I haven't limited the updates.
    for iChunk in xrange(len(dEntities["FlagList"])-1,-1,-1):
        #This will tell the chunk to determine if it is empty or not
        Flag_Update({"chunk":dEntities["FlagList"][iChunk]})

        print "updating flagList!"

        #This removes the pointer from our flag update list.
        dEntities["FlagList"]._Remove(iChunk)

def Update_Render_List(dEntities):
    """Depending on where window is in the world and which chunks are renderable. We will determine which chunks are going to be rendered
    next time rendering occurs."""

    dEntities["RenderList"]._Clear()

    print "These are the world positions of the chunks that are in the render list!"

    #Only the chunks within the window are applicable
    #This will iterate through all of the chunks inside the window at the moment.
    for i in xrange( dEntities["WorldPos"]._Get_X(), dEntities["WorldPos"]._Get_X() + dEntities["ChunksInWind"]._Get_X() ):
        for j in xrange( dEntities["WorldPos"]._Get_Y(), dEntities["WorldPos"]._Get_Y() + dEntities["ChunksInWind"]._Get_Y() ):

            print i, j

            #Check to see if the chunk is loaded and not empty!
            if dEntities["ChunkDict"]["%d,%d"%(i,j)]._Get_Component("FLAG:IsLoaded")._Get_Flag() \
               and not dEntities["ChunkDict"]["%d,%d"%(i,j)]._Get_Component("FLAG:IsEmpty")._Get_Flag():

                print "A chunk is being added to the render List!"

                pChunk = dEntities["ChunkDict"]["%d,%d"%(i,j)]

                #Put the chunk pointer into the render list!
                dEntities["RenderList"]._Add(pChunk)


def Load_Data(dEntities):
    """From the data within the chunk's file, we then give this list of lists as an argument for the Chunk's _Load_Data().
    So from here we'll update the self._tiles list of lists with a list of lists of similar size (the data.)"""

    fileName = os.getcwd() + "\\ChunkData\\" \
                + str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_X()) \
                + " " + str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_Y()) + ".txt"

    failureFlag = False

    tiles = dEntities["chunk"]._Get_Component("LIST:Tiles")

    try:
        fileObj = open(fileName, "r")

        dataBuffer = fileObj.read()

        offset = 0

        for row in xrange(config.CHUNK_TILES_HIGH):
            for col in xrange(config.CHUNK_TILES_WIDE):
                for depth in xrange(config.CHUNK_LAYERS):

                    #The 1d index for the dataBuffer's current number
                    index = ((row*config.CHUNK_TILES_WIDE + col)*config.CHUNK_LAYERS + depth)*3 + offset    #Note that the *3 refers to the spaces taken up by each element in the data file.

                    tiles[row][col][depth]._Set_TileID(int(dataBuffer[index])*10 + int(dataBuffer[index+1]))  #This will not always set a tile to active (if tileType is 0, then it isn't active)

        #Flag that the chunk has been updated with data
        dEntities["chunk"]._Get_Component("FLAG:IsLoaded")._Set_Flag(True)

        fileObj.close()

    except Exception:
        print fileName, "data file wasn't found, so the chunk will be filled in as though empty."

        #If the file doesn't exist, then we can just fill our chunk with transparent tiles!
        for row in xrange(config.CHUNK_TILES_HIGH):
            for col in xrange(config.CHUNK_TILES_WIDE):
                for depth in xrange(config.CHUNK_LAYERS):

                    tiles[row][col][depth]._Set_TileID(0)

def Unload(dEntities):
    """This is where we'll be saving the contents of a chunk to a file."""

    fileName = config.Saved_Game_Directory + "/ChunkData"   \
               + str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_X()) \
               + " " + str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_Y()) + ".txt"

    #try:
    fileObj = open(fileName, "w")       #This won't provoke errors, because the file will either be created or overwritten.

    #The attributes and the tile IDs need to be assembled into a string representation and written to our fileObj

    dataString = ""

    tiles = dEntities["chunk"]._Get_Component("LIST:Tiles")

    for row in xrange(config.CHUNK_TILES_HIGH):
        for col in xrange(config.CHUNK_TILES_WIDE):
            for depth in xrange(config.CHUNK_LAYERS):

                dataString += str(tiles[row][col][depth]) + " "     #This gets our TWO digits for the current tileID and adds a space onto the end of it

    fileObj.write(dataString)

    fileObj.close()     #Without this, there could be a corrupted file
    #except Exception:
        #print fileName, "failed to load, because it does not exist!"

def Flag_Update(dEntities):
    """This will determine if a chunk is empty or not depending on its meshes (a chunk with an empty mesh might as well be empty.)"""
    dEntities["chunk"]._Get_Component("FLAG:IsEmpty")._Set_Flag(True)

    for mesh in dEntities["chunk"]._Get_Component("MESH:0")._Get_Meshes():
        if len(mesh) != 0:
            dEntities["chunk"]._Get_Component("FLAG:IsEmpty")._Set_Flag(False)
            break

def Build_Meshes(dEntities):
    """We create a mesh here using a VertexArray for a chunk that's on the screen. This only is meant to be for chunk's in relation to their position on the screen.
    Chunks off the screen don't need to have their meshes updated for no reason, but they can still have their data loaded before getting onto the screen."""
    #Makes sure that we have an empty vertex array to add to

    dEntities["chunk"]._Get_Component("MESH:0")._Clear_Meshes()

    windowPos = dEntities["chunk"]._Get_Component("POS:WindowPos")._Get_Position()

    windowPos[0] = int(windowPos[0])
    windowPos[1] = int(windowPos[1])
    
    #Handles the building of the tiles within the chunk
    for j in xrange(config.VIEW_TILE_HEIGHT):
        for i in xrange(config.VIEW_TILE_WIDTH):
            #This assumes that depth 0 is the very front of the screen.
            for k in xrange(config.CHUNK_LAYERS):

                if dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_Is_Active():

                    #Calculates the position inside of our window where the tile will be placed
                    tileXPos = (windowPos[0]+i)*config.TILE_SIZE
                    tileYPos = (windowPos[1]+j)*config.TILE_SIZE

                    #Determine the coordinates of the tileType for our tile atlas (TILE_ATLAS_SIZE^2 possible tileTypes) (not working with pixel coords yet)
                    textXPos = (dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_TileID()-1) % config.TILE_ATLAS_SIZE
                    textYPos = (dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_TileID()-1-textXPos) / config.TILE_ATLAS_SIZE

                    #Normalize the texture positions!
                    textXPos *= config.TILE_SIZE
                    textYPos *= config.TILE_SIZE

                    dEntities["chunk"]._Get_Component("MESH:0")._Add_To_Mesh( k, [ sf.Vertex( (tileXPos, tileYPos), sf.Color.WHITE, (textXPos, textYPos) ),  \
                                                                                   sf.Vertex( (tileXPos, tileYPos+config.TILE_SIZE), sf.Color.WHITE, (textXPos, textYPos+config.TILE_SIZE) ),    \
                                                                                   sf.Vertex( (tileXPos+config.TILE_SIZE, tileYPos+config.TILE_SIZE), sf.Color.WHITE, (textXPos+config.TILE_SIZE, textYPos+config.TILE_SIZE) ),  \
                                                                                   sf.Vertex( (tileXPos+config.TILE_SIZE, tileYPos), sf.Color.WHITE, (textXPos+config.TILE_SIZE, textYPos) ) ] )

                    print "ActiveTile!", tileXPos, tileYPos
                    #If this tile isn't partially see-through, then all tiles behind it are occluded and we don't need to add them to their meshes.
                    if dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_Is_Transparent() != True:
                        #This is confirmed to correctly break out of ONLY the CHUNK_LAYERS loop and still allow the other loops to continue.
                        break











