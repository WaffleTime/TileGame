import os, os.path
import random
import shutil
from math import ceil
import sfml as sf
import xml.etree.ElementTree as ET
#This is solely for reparsing xml files to give them indentations so that they are readable..
from xml.dom import minidom
import config
import components
import entities

#This is only necessary because the system functions for altering the tile environment
#   require them to query for the mouse's location.
#from main import window, windowView

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

        #I'm not sure why this was here.
        #for indx in xrange(len(System_Manager.lActionSystems)):
        #    if System_Manager.lActionSystems[indx][0] == sSystemFuncName:
        #        System_Manager.lActionSystems.pop(indx)
        #        break
        
        for indx in xrange(len(System_Manager.lStateSystems)):
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

def Change_Save_Dir(dEntities):
    """This is for switching the directory that is looked in for saved game
    information. That directory contains chunk data, player data and
    entity data."""

    config.Saved_Game_Directory = dEntities["button"]._Get_Component("MISC:Dir")._Get_Storage()

    return "NULL,NULL"

def Change_Map_Dir(dEntities):
    """This is for switching the directory that is looked in for Markov Chain map
    information. That directory contains the data that will be used for generating
    new maps."""

    config.Map_Data_Directory = dEntities["button"]._Get_Component("MISC:Dir")._Get_Storage()

    return "NULL,NULL"


def Determine_Map_Boundaries(dEntities):
    """This  is crucial for the Save_Markov_Map_Data system func. Its purpose is to
    determine the overall boundary (top, left, right, down) for the Chunk data within
    the map that is stored within the config.Map_Data_Directory."""

    #This will be done by just looking at the files within the config.Saved_Game_Directory
    #   with the os module.

    iLeftBound = 0
    iRightBound = 0
    iTopBound = 0
    iBottomBound = 0

    lyst = os.listdir(os.getcwd() + config.Map_Data_Directory)

    for fileName in lyst:

        if fileName[-4:] == ".txt":
            #This will separate the x and y chunk positions and
            #   get rid of the file extension.
            lChunkPos = fileName[0:-4].split(" ")

            if lChunkPos[0] < iLeftBound:

                iLeftBound = int(lChunkPos[0])

            elif lChunkPos[0] > iRightBound:

                iRightBound = int(lChunkPos[0])

            if lChunkPos[1] < iTopBound:

                iTopBound = int(lChunkPos[1])

            elif lChunkPos[1] > iBottomBound:

                iBottomBound = int(lChunkPos[1])

    #So now the boundaries should all be figured out and we just need
    #   to give the data to the entities that the Save_Markov_Map_Data
    #   system function will be referencing when calculating the MC data.

    #NOTE: Since there will automatically be a layer of Chunks around the map that
    #   are empty (the ChunkManager does this no matter what atm,) we will disregard
    #   that outside layer when iterating over the map. And we'll do so by altering
    #   the boundary.

    dEntities["boundary"]._Get_Component("MISC:LeftBound")._Set_Storage(iLeftBound+1)
    dEntities["boundary"]._Get_Component("MISC:RightBound")._Set_Storage(iRightBound-1)
    dEntities["boundary"]._Get_Component("MISC:TopBound")._Set_Storage(iTopBound+1)
    dEntities["boundary"]._Get_Component("MISC:BottomBound")._Set_Storage(iBottomBound-1)

    #This will make our chunk manager move to the top left corner of the boundary.
    Goto_Chunk_Position( {"ChunkMan":dEntities["ChunkMan"],  \
                          "Position":entities.Entity("",  \
                                                     "",  \
                                                     -1,   \
                                                     {"pos":components.Position( {"componentID":"direction",    \
                                                                                  "positionX":iLeftBound+1,             \
                                                                                  "positionY":iTopBound+1} )})} )

    if not os.path.exists(os.getcwd() + config.Map_Data_Directory + "MCData\\"):

        os.mkdir(os.getcwd() + config.Map_Data_Directory + "MCData\\")


    #The Saved_Game_Directory is being used to point to the directory with the ChunkData we're saving as
    #   Markov Chain data.
    lyst = os.listdir(os.getcwd() + config.Map_Data_Directory + "MCData\\")

    for name in lyst:

        if name[-4:] == ".xml":

            #If it exists, then we remove that file.
            os.remove(os.getcwd() + config.Map_Data_Directory + "MCData\\" + name)

    return "NULL,NULL"

def Goto_Chunk_Position(dEntities):
    """This is for making the chunk manager move to the specified position."""

    #Calculate the offset
    xOffset = dEntities["Position"]._Get_Component("POS:direction")._Get_X() - dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_X()
    yOffset = dEntities["Position"]._Get_Component("POS:direction")._Get_Y() - dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_Y()

    #Change position to offset
    dEntities["Position"]._Get_Component("POS:direction")._Set_Position([xOffset, yOffset])

    #Move by offset
    Move_Chunk_Position( {"ChunkMan":dEntities["ChunkMan"],
                          "Offset":dEntities["Position"]})

def Setup_Markov_Data_Files(dEntities):
    """This is meant for checking to see if the Markov data files exist for the Chunk Data that is within the
    config.Map_Data_Directory. If they don't already exist, then we'll create empty files."""

    #Iterate through the relative tile positions available
    for y in xrange(config.TILE_YRELATION_MIN,config.TILE_YRELATION_MAX+1):
        for x in xrange(config.TILE_XRELATION_MIN,config.TILE_XRELATION_MAX+1):

            #This is necessary because it makes no sense to count the 0,0 relative tile for the Markov Chain.
            #   The 0,0 relative tile is the same as the target tile.
            if y == 0 and x == 0:
                continue

            Relation = ET.Element("RelativePosition", {"Relation":"%d,%d"%(x,y)})

            for layer in xrange(config.CHUNK_LAYERS):

                maxTileTypes = 0

                if layer == 0:
                    maxTileTypes = config.FOREGROUND_TILE_TYPES

                elif layer == 1:
                    maxTileTypes = config.GROUND_TILE_TYPES

                elif layer == 2:
                    maxTileTypes = config.BACKGROUND_TILE_TYPES

                Layer = ET.Element("ChunkLayer", {"Layer":"%d"%(layer)})

                #Iterate through the different tile types available for the
                #   relative tile.
                for tileType in xrange(config.GROUND_TILE_TYPES):
                    
                    RelativeTile = ET.Element("RelativeTile", {"TileType":str(tileType)})

                    #Iterate through the different tile types available for the
                    #   target tile.
                    for tileType in xrange(maxTileTypes):

                        TargetTile = ET.Element("TargetTile", {"TileType":str(tileType)})

                        TargetTile.text = "0"
                        
                        RelativeTile.append(TargetTile)

                    Layer.append(RelativeTile)

                Relation.append(Layer)            

            #This will reparse the xml file and give it indentations so that it's readable.
            rough_string = ET.tostring(Relation, 'utf-8')
            
            reparsed = minidom.parseString(rough_string)
            
            prettyRelation = ET.fromstring(reparsed.toprettyxml(indent="    "))

            ET.ElementTree(prettyRelation).write(os.getcwd() + config.Map_Data_Directory + "MCData\\" + "%d,%d.xml"%(x,y))


    return "NULL,NULL"


def Calculate_Markov_Map_Data(dEntities):
    """This is supposed to iterate over the tile data within a map that is made with the
    in-game map editor. And with that data, it is supposed to calculate a number of Markov
    Chains that will later be used to generate the levels for the new saved games. Each
    Markov Chain represents the probability that a tile is a certain tileType given the
    tileType of a tile that is at a relative position. So for each relative position,
    there will be a Markov Chain. The number of relative positions shouldn't be greater than
    config.CHUNK_TILES_WIDE*config.CHUNK_TILES_WIDE."""

    #NOTE: One chunk will be dealt with at a time, because the window needs
    #   to be able to be responsive during the saving of MC data.
    
    #For starters, the directory that we'll be getting our chunk data from will be
    #   represented by config.Saved_Game_Directory.

    #Then starting from the top-left corner, we must iterate over all of the chunks
    #   one chunk at a time.

    #And while iterating over those chunks, we need to calculate Markov Chain data
    #   for each of the tiles within each chunk.

    #Check to see if we don't need to move down to the next row yet.
    if dEntities["ChunkCounter"]._Get_Component("COUNT:x")._Get_Count()   \
       < (dEntities["boundary"]._Get_Component("MISC:RightBound")._Get_Storage() - dEntities["boundary"]._Get_Component("MISC:LeftBound")._Get_Storage() +1):

        dChunkDict = dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict")
        lWorldPos = dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_Position()

        print "Calculating Markov Chain data for chunk position: ", lWorldPos

        TargetChunk = dChunkDict["%d,%d"%(lWorldPos[0], lWorldPos[1])]
        RChunk = dChunkDict["%d,%d"%(lWorldPos[0]+1, lWorldPos[1])]
        DChunk = dChunkDict["%d,%d"%(lWorldPos[0], lWorldPos[1]+1)]
        LChunk = dChunkDict["%d,%d"%(lWorldPos[0]-1, lWorldPos[1])]
        UChunk = dChunkDict["%d,%d"%(lWorldPos[0], lWorldPos[1]-1)]
        URChunk = dChunkDict["%d,%d"%(lWorldPos[0]+1, lWorldPos[1]-1)]
        ULChunk = dChunkDict["%d,%d"%(lWorldPos[0]-1, lWorldPos[1]-1)]
        DRChunk = dChunkDict["%d,%d"%(lWorldPos[0]+1, lWorldPos[1]+1)]
        DLChunk = dChunkDict["%d,%d"%(lWorldPos[0]-1, lWorldPos[1]+1)]


        #So now we'll iterate through all of the tiles within the current chunkkkkkkk,
        for y in xrange(config.CHUNK_TILES_HIGH):
            for x in xrange(config.CHUNK_TILES_WIDE):
                for z in xrange(config.CHUNK_LAYERS):

                    #print "Saving MC data for a tile %d,%d,%d"%(y,x,z)

                    #Then for each one of those tiles, we'll have to iterate through the relative tile positions
                    for yRelation in xrange(y+config.TILE_YRELATION_MIN, y+config.TILE_YRELATION_MAX+1):
                        for xRelation in xrange(x+config.TILE_XRELATION_MIN, x+config.TILE_XRELATION_MAX+1):

                            #This is necessary because it makes no sense to count the 0,0 relative tile for the Markov Chain.
                            #   The 0,0 relative tile is the same as the target tile.
                            if (yRelation-y == 0) and (xRelation-x == 0):
                                continue
                            
                            #To see if the tile in relation exists, we
                            #   must know the chunk that it is on.
                            #This checks to see if the relation is within the Chunk that is being
                            #   generated.
                            if (yRelation >= 0 and yRelation < config.CHUNK_TILES_HIGH) \
                                and (xRelation >= 0 and xRelation < config.CHUNK_TILES_WIDE):

                                if not TargetChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation][xRelation][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()
                                    
                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation][xRelation][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()
                                
                            #If the relation isn't within the chunk, then it must be within a neighboring chunk.
                            #So we'll first check to see if the right chunk has the relation position.
                            elif (yRelation >= 0 and yRelation < config.CHUNK_TILES_HIGH)   \
                                and (xRelation >= config.CHUNK_TILES_WIDE):

                                if not RChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation][xRelation-config.CHUNK_TILES_WIDE][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()
                                    
                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation][xRelation-config.CHUNK_TILES_WIDE][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()

                            #Then we'll check to see if the down chunk has the relation position.
                            elif (yRelation >= config.CHUNK_TILES_HIGH) \
                                and (xRelation >= 0 and xRelation < config.CHUNK_TILES_WIDE):

                                if not DChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][xRelation][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()
                                    
                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][xRelation][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()

                            #Then we'll check to see if the left chunk has the relation position.
                            elif (yRelation >= 0 and yRelation < config.CHUNK_TILES_HIGH)   \
                                and (xRelation < 0):

                                if not LChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation][(-1*xRelation)-1][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()
                                    
                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation][(-1*xRelation)-1][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()
                                    
                            #Then we'll check to see if the up chunk has the relation position.
                            elif (yRelation < 0)    \
                                and (xRelation >= 0 and xRelation < config.CHUNK_TILES_WIDE):

                                if not UChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][xRelation][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()
                                    
                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][xRelation][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()

                            #Then we'll check to see if the up right chunk has the relation position.
                            elif (yRelation < 0)    \
                                and (xRelation >= config.CHUNK_TILES_WIDE):

                                if not URChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][xRelation-config.CHUNK_TILES_WIDE][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()
                                    
                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][xRelation-config.CHUNK_TILES_WIDE][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()

                            #Then we'll check to see if the up left chunk has the relation position.
                            elif (yRelation < 0)    \
                                and (xRelation < 0):

                                if not ULChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][(-1*xRelation)-1][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()

                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][(-1*xRelation)-1][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()

                            #Then we'll check to see if the down right chunk has the relation position.
                            elif (yRelation >= config.CHUNK_TILES_HIGH) \
                                and (xRelation >= config.CHUNK_TILES_WIDE):

                                if not DRChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                    
                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][xRelation-config.CHUNK_TILES_WIDE][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()

                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][xRelation-config.CHUNK_TILES_WIDE][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()

                            #Then we'll check to see if the down left chunk has the relation position.
                            elif (yRelation >= config.CHUNK_TILES_HIGH) \
                                and (xRelation < 0):

                                if not DLChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():

                                    #This increments the MCData counter for the current tileType transition.
                                    dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][(-1*xRelation)-1][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Increment()
                                    
                                    #print "Incrementing relation %d,%d to"%(xRelation-x,yRelation-y), dEntities["MCData"]._Get_Component("LIST:MCData")[z][yRelation-y][xRelation-x][TargetChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][(-1*xRelation)-1][1]._Get_TileID()][TargetChunk._Get_Component("LIST:Tiles")[y][x][z]._Get_TileID()]._Get_Count()

                            else:

                                print "The Save_Markov_Data() system function should not have entered this else, because all of the cases should have been covered for where  \
                                        the relative tile is located!"


        dEntities["ChunkCounter"]._Get_Component("COUNT:x")._Increment()

        #Move by offset to the right one chunk.
        Move_Chunk_Position( {"ChunkMan":dEntities["ChunkMan"],
                              "Offset":entities.Entity("",  \
                                                       "",  \
                                                       -1,   \
                                                       {"pos":components.Position( {"componentID":"direction",    \
                                                                                    "positionX":1,             \
                                                                                    "positionY":0} )})} )

    else:

        if dEntities["ChunkCounter"]._Get_Component("COUNT:y")._Get_Count()   \
           < (dEntities["boundary"]._Get_Component("MISC:BottomBound")._Get_Storage() - dEntities["boundary"]._Get_Component("MISC:TopBound")._Get_Storage() +1):

            dEntities["ChunkCounter"]._Get_Component("COUNT:y")._Increment()
            dEntities["ChunkCounter"]._Get_Component("COUNT:x")._Reset_Counter()

            #This will make our chunk manager move to the beginning of the next row down.
            Goto_Chunk_Position( {"ChunkMan":dEntities["ChunkMan"],  \
                                  "Position":entities.Entity("",  \
                                                             "",  \
                                                             -1,   \
                                                             {"pos":components.Position( {"componentID":"direction",    \
                                                                                          "positionX":dEntities["boundary"]._Get_Component("MISC:LeftBound")._Get_Storage(),             \
                                                                                          "positionY":dEntities["boundary"]._Get_Component("MISC:TopBound")._Get_Storage()               \
                                                                                                      + dEntities["ChunkCounter"]._Get_Component("COUNT:y")._Get_Count()} )})} )

        else:

            #We're done with this system function, so we'll remove it.
            System_Manager._Remove_State_System("Calculate_Markov_Map_Data")

            #Before being done with all of this, we first need to convert the data
            #   within the .xml file we just filled so that its usable Markov Chain data.
            #All of the transitions from a single tileType need to add up to one (because
            #   there's a 100% change that another tileType is chosen.)

            #So we need to add the system function that will be used for saving that data.
            System_Manager._Add_System("state", "Save_Markov_Map_Data", [ ("Storage", "MCData", "MCData"), ("Storage", "Counter", "TileRelationCounter") ])

            #These are being reset so that the Save_Markov_Map_Data can reuse the counters for the tile relations
            #   (because one tile relation will be normalized and saved at a time.)
            dEntities["ChunkCounter"]._Get_Component("COUNT:x")._Set_Counter(config.TILE_XRELATION_MIN)
            dEntities["ChunkCounter"]._Get_Component("COUNT:y")._Set_Counter(config.TILE_YRELATION_MIN)


    return "NULL,NULL"

def Save_Markov_Map_Data(dEntities):
    """This will simply save the TileType transition data to the xml files for the
    Markov Chain. But the data at this point isn't normalized, so we'll have to normalize
    it as we go. Then afterward, the Markov Chain data will be ready to be used for the
    generation of maps."""


    #Here we check to see if we're within the bounds of the tile relation area we
    #   are interested in.
    if dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count()      \
       <= config.TILE_XRELATION_MAX:

        #This just makes sure that we're going to ignore the 0,0 tile relation,
        #   because that represents the transition from one spot to the same spot (we don't want that.)
        if dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count() != 0     \
           and dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count() != 0:

            print "Saving %d,%d tile relation MCData"%(dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count(),dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count())

            MCTree = ET.parse(os.getcwd() + config.Map_Data_Directory + "MCData\\" + "%d,%d.xml"%(dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count(),dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count()))

            MCRoot = MCTree.getroot()
            
            #Here is where we must normalize and save the xml data for the tile relation
            #   that we are currently on. (Note that only one tile relation is handled at a time!)
            #Each layer has its own individual tile relation data.
            for layer in xrange(config.CHUNK_LAYERS):

                layerXMLData = MCRoot.find("ChunkLayer[@Layer='%d']"%layer)

                #Notice that we're always dealing with the tileTypes of the ground layer when
                #   we're iterating through the prevTileTypes (which are the tileTypes that
                #   we're transitioning from.) This is because each layer is to be generated with
                #   respect to the ground layer.
                for prevTileType in xrange(config.GROUND_TILE_TYPES):

                    prevTileTypeXMLData = layerXMLData.find("RelativeTile[@TileType='%d']"%prevTileType)

                    #Before looping through the tile types that we're transitioning to,
                    #   we must know the tileTypes that are available with respect to the
                    #   chunk layer (the tileTypes we're transitioning to are variable,
                    #   while the tileTypes we're transitioning from are constant.)

                    maxTileTypes = 0

                    #Check if we're transitiong to the foreground layer 
                    if layer == 0:
                        maxTileTypes = config.FOREGROUND_TILE_TYPES

                    #Check if we're transitiong to the ground layer 
                    elif layer == 1:
                        maxTileTypes = config.GROUND_TILE_TYPES
                        
                    #Check if we're transitiong to the background layer 
                    elif layer == 2:
                        maxTileTypes = config.BACKGROUND_TILE_TYPES

                    totalTransitions = 0.

                    #This is saved just so that the huge thing of embedded lists doesn't have to keep being queried.
                    #So now this is a list of transition data for the current layer, tile relation and prevTileType.
                    nextTileTypeMCData = dEntities["MCData"]._Get_Component("LIST:MCData")[layer][dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count()][dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count()][prevTileType]
                        
                    #For each state within a tile relation, we must add up the transitions from that state.
                    #   Then we can use that number to normalize the transition probabilities with respect
                    #   to that state.
                    #After this for loop is done, we have the total transitions and can begin normalizing.
                    for nextTileType in xrange(maxTileTypes):
 
                        totalTransitions += nextTileTypeMCData[nextTileType]._Get_Count()

                    #print "The tile relation %d,%d now has %d total transitions for the prevTileType %d"%(dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count(),dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count(),totalTransitions,prevTileType)

                    #This prevents division by zero for the normalizing process (the transitions are normalized already in a sense too,
                    #   because they are already at zero or zero percent probability.)
                    if totalTransitions != 0:

                        #Then we must divide each transition by the total number of transitions and that
                        #   will give us our normalized transition probability.
                        for nextTileType in xrange(maxTileTypes):

                            #Here we're just normalizing the transition data for each transition from the current prevTileType, layer and tile relation.
                            nextTileTypeMCData[nextTileType]._Set_Counter(float(nextTileTypeMCData[nextTileType]._Get_Count())/totalTransitions)

                            prevTileTypeXMLData.find("TargetTile[@TileType='%d']"%nextTileType).text = str(nextTileTypeMCData[nextTileType]._Get_Count())

                            #print "The tile relation %d,%d has %f probability of transitioning from %d prevTileType to %d nextTileType on layer %d"%(dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count(),dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count(),nextTileTypeMCData[nextTileType]._Get_Count(),prevTileType,nextTileType,layer)

            #This saves the MCData that we just added to the xml file for the current tile relation.
            MCTree.write(os.getcwd() + config.Map_Data_Directory + "MCData\\" + "%d,%d.xml"%(dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Get_Count(),dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count()))

        #This will increment the tile relation counter outside of the previous if statement, because it prevents
        #   us from being stuck at tile relation (0,0) forever.
        dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Increment()

    else:

        dEntities["TileRelationCounter"]._Get_Component("COUNT:x")._Set_Counter(config.TILE_XRELATION_MIN)
        dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Increment()

        #Here we check to see if we're outside the bounds of the tile relation area we are
        #   interested in.
        if dEntities["TileRelationCounter"]._Get_Component("COUNT:y")._Get_Count()      \
           > config.TILE_YRELATION_MAX:

            #Once we hit here, this whole system function is complete and we can remove it from the
            #   System_Manager
            System_Manager._Remove_State_System("Save_Markov_Map_Data")

            return "Menu,MainMenu"
       

    return "NULL,NULL"
    

def New_Save(dEntities):
    """This will setup a new saved game directory along with the player's
    xml data. Along with this system there should be other functions
    that will move the chunk data into this directory and also
    fetch the entity xml data for the beginning level."""

    previousDirectory = os.getcwd()

    os.chdir(os.getcwd() + "\\SavedGames\\")

    lyst = os.listdir(os.getcwd())

    counter = 0

    #print lyst

    #Iterate through the lyst counting the saved games.
    for i in lyst:
        #Checks if the current item
        #   is a Saved Game dir.
        if (i[0:4] == "Save"):
            counter += 1
            #print counter, i[0:4]

    #This is so that the counter is one more than the total
    #   amount of saves.
    counter += 1

    #This is the new saved game's folder
    os.mkdir(os.getcwd() +"\\Save" + str(counter))

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
    playerStats.find("CurHp").text = "20"
    playerStats.append(ET.Element("MaxHp"))
    playerStats.find("MaxHp").text = "20"

    playerStats.append(ET.Element("CurMp"))
    playerStats.find("CurMp").text = "20"
    playerStats.append(ET.Element("MaxMp"))
    playerStats.find("MaxMp").text = "20"

    playerStats.append(ET.Element("Strength"))
    playerStats.find("Strength").text = "10"
    playerStats.append(ET.Element("Intelligence"))
    playerStats.find("Intelligence").text = "10"
    playerStats.append(ET.Element("Dexterity"))
    playerStats.find("Dexterity").text = "10"
    playerStats.append(ET.Element("Agility"))
    playerStats.find("Agility").text = "10"

    #This should save the xml we just created
    #   into the new saved directory
    ET.ElementTree(playerStats).write("PlayerData.xml")

    #Select this new saved game.
    config.Saved_Game_Directory = "\\SavedGames\\Save" + str(counter) + "\\ChunkData\\"

    #This will change the directory back to what it was originally.
    os.chdir(previousDirectory)

    os.mkdir("%s%s"%(os.getcwd(), config.Saved_Game_Directory))

    shutil.copy2("%s\\Resources\\ChunkData\\NewSave\\0 0.txt"%os.getcwd(),
                 "%s%s"%(os.getcwd(), config.Saved_Game_Directory))

    shutil.copy2("%s\\Resources\\ChunkData\\NewSave\\0 1.txt"%os.getcwd(),
                 "%s%s"%(os.getcwd(), config.Saved_Game_Directory))

    shutil.copy2("%s\\Resources\\ChunkData\\NewSave\\1 0.txt"%os.getcwd(),
                 "%s%s"%(os.getcwd(), config.Saved_Game_Directory))

    shutil.copy2("%s\\Resources\\ChunkData\\NewSave\\1 1.txt"%os.getcwd(),
                 "%s%s"%(os.getcwd(), config.Saved_Game_Directory))

    #Here we're going to change the frame rate of the game so that the main() doesn't think it
    #   always needs to catch up with realtime.
    iFrameRate = config.FRAME_RATE
    config.FRAME_RATE = config.LOADING_FRAME_RATE
    config.LOADING_FRAME_RATE = iFrameRate

    return "NULL,NULL"

def Load_MCData(dEntities):
    """This is for loading the MCData from the xml files into an entity that will be used to generate
    the chunk data for the new saved game. This is done because it's much faster to query data from an
    entity object than from the harddrive (RAM vs Harddrive.) This system function will also load in the
    starting chunks for the ChunkManager entity. That is done because there is no Update() system function
    being used during the course of the NewGame state. Instead Update() is only being called when it needs
    to be within the Generate_World_Data() system function."""

    #Gotta fill up that MCData entity with the xml data!
    for y in xrange(config.TILE_YRELATION_MIN,config.TILE_YRELATION_MAX+1):
        
        for x in xrange(config.TILE_XRELATION_MIN,config.TILE_XRELATION_MAX+1):

            if y == 0 and x == 0:
                continue
            
            #Luoad the xml data for the tileRelation.
            MCTree = ET.parse(os.getcwd() + config.Map_Data_Directory + "%d,%d.xml"%(x,y))

            MCRoot = MCTree.getroot()

            for layer in xrange(config.CHUNK_LAYERS):

                xmlLayer = MCRoot.find("ChunkLayer[@Layer='%d']"%layer)

                for prevTileType in xrange(config.GROUND_TILE_TYPES):

                    xmlPrevTileType = xmlLayer.find("RelativeTile[@TileType='%d']"%prevTileType)

                    if layer == 0:

                        for targetTileType in xrange(config.FOREGROUND_TILE_TYPES):

                            dEntities["MCData"]._Get_Component("LIST:MCData")[layer][y][x][prevTileType][targetTileType]._Set_Counter(float(xmlPrevTileType.find("TargetTile[@TileType='%d']"%targetTileType).text))

                    if layer == 1:

                        for targetTileType in xrange(config.GROUND_TILE_TYPES):

                            dEntities["MCData"]._Get_Component("LIST:MCData")[layer][y][x][prevTileType][targetTileType]._Set_Counter(float(xmlPrevTileType.find("TargetTile[@TileType='%d']"%targetTileType).text))

                    if layer == 2:

                        for targetTileType in xrange(config.BACKGROUND_TILE_TYPES):

                            dEntities["MCData"]._Get_Component("LIST:MCData")[layer][y][x][prevTileType][targetTileType]._Set_Counter(float(xmlPrevTileType.find("TargetTile[@TileType='%d']"%targetTileType).text))



    Update_Load_List({"LoadList":dEntities["ChunkMan"]._Get_Component("LIST:LoadList"),                 \
                      "ChunkDataDir":dEntities["ChunkMan"]._Get_Component("MISC:ChunkDataDir")})

    return "NULL,NULL"

def Generate_World_Data(dEntities):
    """This will generate level data for the current saved game. And the ChunkData will be
    saved inside the saved game's directory. Note that this function is designed to only
    generate chunk data for a limited amount of chunks (that way a loading screen
    can be displayed as the chunks are generated, this is so the user doesn't
    freak out when the program doesn't respond.)

    My Idea for generating the levels so far is:

    1. Copy four generic chunks into the \\ChunkData\\. It only needs a platform for the
    player to spawn on (this is now done in New_Save().)

    1A. (optional) Copy in empty Chunks to stop the generationg of levels to get too crazy. The empty
    chunks should be exist Y chunks above the player and make a horizontal line X chunks in width.

    2. Generate Chunks around the first chunks that were copied in. There should be a separate system
    function that will take in chunks"""


    #Depending on the chunk that will be generated, there will be different chunks
    #   that are able to be used for determining the new tiles. So we need a way
    #   to gather up the chunks that are already built.

    #The Chunk that needs to be generated should be one of the four chunks in the center
    #   of the chunk manager's view. That way, there is a ring of chunks around it
    #   and they can be used for generating the data. That means that we won't have to watch
    #   out for chunks that don't exist within the Chunk Manager's ChunkDict when getting
    #   the chunk data for the chunk to be generated. But some of those chunks will turn out
    #   to be empty.


    #This counts the sides of the spiral that have been generated.
    iSpiralOffset = dEntities["MoveCounter"]._Get_Component("COUNT:spiralSideCount")._Get_Count()
    fMoveOffset = float(dEntities["MoveCounter"]._Get_Component("COUNT:moveCount")._Get_Count())
    iCurrentChunk = dEntities["MoveCounter"]._Get_Component("COUNT:chunkCount")._Get_Count()

    #Right, down, left, up
    lOrderOfOffsetsX = [1, 0, -1, 0]
    lOrderOfOffsetsY = [0, 1, 0, -1]


    #print "The current spiral side offset is %d" % (iSpiralOffset)
    #print "The current move offset is %d" % (fMoveOffset)

    if iSpiralOffset < int(dEntities["MoveCounter"]._Get_Component("MISC:maxMoves")._Get_Storage()):

        #This checks to see if we still have to generate more chunks fo the
        #   current side of the spiral.
        if fMoveOffset < ceil((iSpiralOffset+1)/2.):

            #This checks to see if we are ready to move onto a new duo of Chunks.
            #   (Because we will generate one chunk at a time and there are two
            #   chunks that need generated for each move we make.)
            if iCurrentChunk == 0:
                #These two moves will move the chunk manager over four new chunks.
                Move_Chunk_Position( {"ChunkMan":dEntities["ChunkMan"],
                                      "Offset":entities.Entity("",  \
                                                       "",  \
                                                       1,   \
                                                       {"pos":components.Position( {"componentID":"direction",    \
                                                                 "positionX":lOrderOfOffsetsX[iSpiralOffset%4],             \
                                                                 "positionY":lOrderOfOffsetsY[iSpiralOffset%4]} )})} )

                #This is called here, because it will speed up the world generation if this is called
                #   only when it needs to be (and that's right after the chunk position is moved.)
                Update({"ChunkMan":dEntities["ChunkMan"]})

                #print "World Position after offset is", dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_Position()

            xChunk = 0
            yChunk = 0

            #Check to see if we just moved to the right one chunk.
            if iSpiralOffset%4 == 0:

                xChunk = 1
                yChunk = 1-iCurrentChunk

            #Check to see if we just moved to the down one chunk.
            elif iSpiralOffset%4 == 1:

                xChunk = iCurrentChunk
                yChunk = 1

            #Check to see if we just moved to the left one chunk.
            elif iSpiralOffset%4 == 2:
                
                xChunk = 0
                yChunk = iCurrentChunk

            #Check to see if we just moved to the up one chunk.
            elif iSpiralOffset%4 == 3:

                xChunk = 1-iCurrentChunk
                yChunk = 0
            
            #print "ChunkPosition in window being generated", xChunk, yChunk

            Generate_Chunk_Data( {"ChunkMan":dEntities["ChunkMan"],      \
                                  "TargetWindowPos":(xChunk,yChunk),     \
                                  "MCData":dEntities["MCData"]} )

            if iCurrentChunk == 0:
                dEntities["MoveCounter"]._Get_Component("COUNT:chunkCount")._Increment()
            else:
                dEntities["MoveCounter"]._Get_Component("COUNT:chunkCount")._Reset_Counter()
                
                #After generating chunks for the current area, we need to increment the move counter
                #   for the current side of the spiral.
                #Everything was setup to move two chunks at a time, so the move offset only gets updated
                #   by 0.5 now (we're now moving one chunk at a time.)
                dEntities["MoveCounter"]._Get_Component("COUNT:moveCount")._Add(0.5)

        #This is entered when the current side of the spiral is complete
        else:
            #Here's where we'll increment our counter component.
            #This counts the directional moves (moving more than once in one direction
            #   counts as a single move. So we increment after generating a row/column of chunks
            #   and those rows/columns will increase in size by 2 chunks every two move counts.)
            dEntities["MoveCounter"]._Get_Component("COUNT:spiralSideCount")._Increment()

            #We also have to reset our move counter for the next side of the spiral.
            dEntities["MoveCounter"]._Get_Component("COUNT:moveCount")._Reset_Counter()

    #When this is entered, the generation will be complete
    else:
        
        #ImportantNote: The last 12 chunks won't be saved unless the world chunk position is moved 4
        #   chunks over (assuming any situation, that basically just loads a completely new area into
        #   the game while simultaneously saving the last area.)
        Move_Chunk_Position( {"ChunkMan":dEntities["ChunkMan"],
                              "Offset":entities.Entity("",  \
                                                       "",  \
                                                       1,   \
                                                       {"pos":components.Position( {"componentID":"direction",    \
                                                                 "positionX":4,             \
                                                                 "positionY":0} )})} )

        Update({"ChunkMan":dEntities["ChunkMan"]})

        #And once we reach this point, the generation is done, so
        #   we need to remove this system function from the System_Manager.
        System_Manager._Remove_State_System("Generate_World_Data")

        #Since we're done with the world generation, we can reset the frame rate back
        #   to what it originally was.
        iLoadFrameRate = config.LOADING_FRAME_RATE
        config.LOADING_FRAME_RATE = config.FRAME_RATE
        config.FRAME_RATE = iLoadFrameRate
        

        #After doing this, we should also change the state to the new saved game!
        #Since the config.Saved_Game_Directory was set in New_Save(), we can
        #   just switch to the continue state to start the new game.
        return "Game,Continue"

    return "NULL,NULL"
        

def Generate_Chunk_Data(dEntities):
    """This should take in a chunk entity that is going to be filled. And all the rest
    of the chunk entities are going to be Chunks that have a relationship with the
    chunk that is to be filled."""

    dChunkDict = dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict")
    lWorldPos = dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_Position()

    tWindowPos = dEntities["TargetWindowPos"]

    TargetChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0], lWorldPos[1]+tWindowPos[1])]
    RChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0]+1, lWorldPos[1]+tWindowPos[1])]
    DChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0], lWorldPos[1]+tWindowPos[1]+1)]
    LChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0]-1, lWorldPos[1]+tWindowPos[1])]
    UChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0], lWorldPos[1]+tWindowPos[1]-1)]
    URChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0]+1, lWorldPos[1]+tWindowPos[1]-1)]
    ULChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0]-1, lWorldPos[1]+tWindowPos[1]-1)]
    DRChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0]+1, lWorldPos[1]+tWindowPos[1]+1)]
    DLChunk = dChunkDict["%d,%d"%(lWorldPos[0]+tWindowPos[0]-1, lWorldPos[1]+tWindowPos[1]+1)]

    #These variables will help decide which area we should start
    #   from when generating tiles (the algorithm will work better
    #   when there are non-empty chunkss close to the tiles that are
    #   being generated first.)

    #Each element represents a position within the target chunk that
    #   we'll start at.
    #topLeft, topRight, bottomLeft, bottomRight
    lVotes = [0, 0, 0, 0]

    #These checks will resultingly vote for the area that we'll start
    #   the generation in.

    if (not LChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[0] += 1
        lVotes[2] += 1

    if (not RChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[1] += 1
        lVotes[3] += 1

    if (not DChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[3] += 1
        lVotes[2] += 1

    if (not UChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[0] += 1
        lVotes[1] += 1

    if (not DLChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[2] += 1

    if (not ULChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[0] += 1

    if (not DRChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[3] += 1

    if (not URChunk._Get_Component("FLAG:IsEmpty")._Get_Flag()):
        #Vote for the relevant starting areas
        lVotes[1] += 1


    #Now we must determine which vote got the highest number (ties don't matter.)

    iGreatestIndx = 0
    iGreatestVotes = 0

    for indx in xrange(len(lVotes)):

        #The strictly greater than will favor the top areas over the bottom.
        if lVotes[indx] > iGreatestVotes:

            iGreatestIndx = indx
            iGreatestVotes = lVotes[indx]

    iStartX = 0
    iEndX = 0
    iStepX = 1
    

    iStartY = 0
    iEndY = 0
    iStepY = 1

    #Check to see if topLeft is the area we'll start in.
    if iGreatestIndx == 0:
        #Since the left and upper chunks aren't empty
        #We will start the generation from the left and upper corner.
        iStartX = 0
        iEndX = config.CHUNK_TILES_WIDE
        iStepX = 1

        iStartY = 0
        iEndY = config.CHUNK_TILES_HIGH
        iStepY = 1

    #Check to see if bottomLeft is the area we'll start in.
    elif iGreatestIndx == 2:
        #Since the left and down chunks aren't empty
        #We will start the generation from the left and down corner.
        iStartX = 0
        iEndX = config.CHUNK_TILES_WIDE
        iStepX = 1

        iStartY = config.CHUNK_TILES_HIGH-1
        iEndY = -1
        iStepY = -1


    #Check to see if topRight is the area we'll start in.
    elif iGreatestIndx == 1:
        #Since the right and upper chunks aren't empty
        #We will start the generation from the right and upper corner.
        iStartX = config.CHUNK_TILES_WIDE-1
        iEndX = -1
        iStepX = -1

        iStartY = 0
        iEndY = config.CHUNK_TILES_HIGH
        iStepY = 1

    #Check to see if bottomRight is the area we'll start in.
    elif iGreatestIndx == 3:
        #Since the right and down chunks aren't empty
        #We will start the generation from the right and down corner.
        iStartX = config.CHUNK_TILES_WIDE-1
        iEndX = -1
        iStepX = -1

        iStartY = config.CHUNK_TILES_HIGH-1
        iEndY = -1
        iStepY = -1

    #This will be what we pass to Alter_Tiles()
    #   after we figure out what the tiles will be changed to.
    lTiles = []

    #Then iterate through the tiles within the Chunk accordingly.
    #The tiles don't need their world position in order to
    #   access the tiles.
    for y in xrange(iStartY, iEndY, iStepY):
        for x in xrange(iStartX, iEndX, iStepX):
            for z in xrange(config.CHUNK_LAYERS):
                #This will hold all the tileTypes that
                #   were generated.
                lTileTypes = []
                
                #Now we'll iterate through the compatible position
                #   relations for the Markov Chains.
                for yRelation in xrange(y+config.TILE_YRELATION_MIN, y+config.TILE_YRELATION_MAX+1):
                    for xRelation in xrange(x+config.TILE_XRELATION_MIN, x+config.TILE_XRELATION_MAX+1):

                        #This is necessary because it makes no sense to count the 0,0 relative tile for the Markov Chain.
                        #   The 0,0 relative tile is the same as the target tile.
                        if (yRelation-y == 0) and (xRelation-x == 0):
                            continue
                        
                        #To see if the tile in relation exists, we
                        #   must know the chunk that it is on.
                        #This checks to see if the relation is within the Chunk that is being
                        #   generated.
                        if (yRelation >= 0 and yRelation < config.CHUNK_TILES_HIGH) \
                            and (xRelation >= 0 and xRelation < config.CHUNK_TILES_WIDE):
                            #So then we can check to see if the tile in this relation has
                            #   been generated yet.
                            #This checks to see if the yRelation shows that the tile may have
                            #    been generated already.
                            #If it hasn't already been generated, we'll ignore it.
                            if ( (y - yRelation)*iStepY >= 0 ):
                                #This checks to see if the xRelation shows that the tile may have
                                #    been generated already.
                                if ( (x - xRelation)*iStepX >= 0 ):
                                    #This should only execute when we know the tile exists for
                                    #   the particular relation.
                                    #Here we get a random (weighted by markov chain) tileType
                                    #   that will be added to a list of tileTypes
                                    lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                      TargetChunk._Get_Component("LIST:Tiles")[yRelation][xRelation][z]._Get_TileID(),   \
                                                                                      z,                            \
                                                                                      dEntities["MCData"]) )


                        #If the relation isn't within the chunk, then it must be within a neighboring chunk.
                        #So we'll first check to see if the right chunk has the relation position.
                        elif (yRelation >= 0 and yRelation < config.CHUNK_TILES_HIGH)   \
                            and (xRelation >= config.CHUNK_TILES_WIDE):

                            if not RChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  RChunk._Get_Component("LIST:Tiles")[yRelation][xRelation-config.CHUNK_TILES_WIDE][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                        #Then we'll check to see if the down chunk has the relation position.
                        elif (yRelation >= config.CHUNK_TILES_HIGH) \
                            and (xRelation >= 0 and xRelation < config.CHUNK_TILES_WIDE):

                            if not DChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  DChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][xRelation][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                        #Then we'll check to see if the left chunk has the relation position.
                        elif (yRelation >= 0 and yRelation < config.CHUNK_TILES_HIGH)   \
                            and (xRelation < 0):

                            if not LChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  LChunk._Get_Component("LIST:Tiles")[yRelation][(-1*xRelation)-1][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                        #Then we'll check to see if the up chunk has the relation position.
                        elif (yRelation < 0)    \
                            and (xRelation >= 0 and xRelation < config.CHUNK_TILES_WIDE):

                            if not UChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  UChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][xRelation][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                        #Then we'll check to see if the up right chunk has the relation position.
                        elif (yRelation < 0)    \
                            and (xRelation >= config.CHUNK_TILES_WIDE):

                            if not URChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  URChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][xRelation-config.CHUNK_TILES_WIDE][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                        #Then we'll check to see if the up left chunk has the relation position.
                        elif (yRelation < 0)    \
                            and (xRelation < 0):

                            if not ULChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  ULChunk._Get_Component("LIST:Tiles")[(-1*yRelation)-1][(-1*yRelation)-1][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                        #Then we'll check to see if the down right chunk has the relation position.
                        elif (yRelation >= config.CHUNK_TILES_HIGH) \
                            and (xRelation >= config.CHUNK_TILES_WIDE):

                            if not DRChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  DRChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][xRelation-config.CHUNK_TILES_WIDE][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                        #Then we'll check to see if the down left chunk has the relation position.
                        elif (yRelation >= config.CHUNK_TILES_HIGH) \
                            and (xRelation < 0):

                            if not DLChunk._Get_Component("FLAG:IsEmpty")._Get_Flag():
                                lTileTypes.append( Calc_New_TileType_For_Relation([xRelation-x, yRelation-y],   \
                                                                                  DLChunk._Get_Component("LIST:Tiles")[yRelation-config.CHUNK_TILES_HIGH][(-1*xRelation)-1][z]._Get_TileID(),   \
                                                                                  z,                            \
                                                                                  dEntities["MCData"]) )

                newTileType = Determine_Majority_TileType(lTileTypes)

                #if newTileType != 0:
                    #print "This tileType isn't zero! newTileType:", newTileType

                lTiles.append( (x + dEntities["TargetWindowPos"][0]*config.CHUNK_TILES_WIDE,    \
                                y + dEntities["TargetWindowPos"][1]*config.CHUNK_TILES_HIGH,    \
                                z,                                                              \
                                newTileType) )

    #print "New Tiles", lTiles

    #This will finally alter the tile data for the tiles in the target chunk.
    Alter_Tiles( {"lTileData":lTiles,                               \
                  "ChunkMan":dEntities["ChunkMan"]} )

    #lWorldPos = dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_Position()

    #print "This tileID should be 1",

    #print dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict")["%d,%d"%(dEntities["TargetWindowPos"][0]+lWorldPos[0],dEntities["TargetWindowPos"][1]+lWorldPos[1])]._Get_Component("LIST:Tiles")[0][0][1]


def Determine_Majority_TileType(lTileTypes):
    """This should sort through the different tileTypes
    that were generated from the different Markov Chains
    for a particular tile and determine the tileType that
    should  be chosen for the tile to be generated.
    @param lTileTypes This is the list of tileTypes that
        will be used to determine the Majority tileType.
    @return A tileType integer that represents the
        new tileType."""

    dDetectedTileTypes = {}

    for tileType in lTileTypes:

        #There are some tileTypes that may be None.
        #   that means that there wasn't a possible tileType
        #   transition for a given relation and prevTileType.
        #   So we skip these instances.
        if tileType == None:
            continue

        if (dDetectedTileTypes.get(tileType, None) == None):

            dDetectedTileTypes[tileType] = 1

        else:

            dDetectedTileTypes[tileType] += 1

    iMostProminentTileType = 0

    iTileTypeOccurrences = 0

    for (iTileType, iOccurrences) in dDetectedTileTypes.items():

        if (iOccurrences > iTileTypeOccurrences):

            iMostProminentTileType = iTileType

            iTileTypeOccurrences = iOccurrences

    return iMostProminentTileType

def Calc_New_TileType_For_Relation(lTileRelation, iPrevTileType, iChunkLayer, MCData):
    """This is for calculating the new tileType
    with the Markov Chain data that was for a particular
    relationship between tile positions.
    @param lTileRelation This is a list of numbers that will be
        used to find the Markov Chain data in the Game's directory.
        It refers to the position relation between the previous tile
        and the tile that is to be generated.
    @param iPrevTileType This is the tileType of the previous tile
        in the Markov Chain. Te Markov Chain's states are
        represented by tileTypes and the Markov Chain that is
        used represents the tile position relation.
    @param iChunkLayer This is the chunk layer that the tileType will
        be generated for.
    @param MCData This is an Entity that holds the Markov Chain data
        for the tile transitions. The data was loaded into it from
        the xml files that were created by the map editor. This
        is just meant to bypass the need for loading the xml files
        a bunch (RAM is faster than the Harddrive in retrieval.)
    @return A tileType integer that represents
        the new tileType."""

    #Randomly pick a tileType based off of the Markov Chain data in the parts that follow.

    #This will be used to count the probabilities of the transitions to targetTileTypes that we're iterating over.
    #This number will equal one at maximum, because all of the transition probabilities add up to one.
    totalProbability = 0.

    #This gets us a random floating point number between [0.,1.).
    #This will be used to determine the targetTileType.
    #   We'll do that by adding up transition probabilities until
    #   we find a probability, that when added to totalProbability,
    #   makes totalProbability greater than randomProbability (assuming it
    #   was previously smaller.)
    randomProbability = random.random()

    #This will be initialized as None in case there wasn't a tileType transition available for the prevTileType on this relation.
    #None will represent when there wan't a possible tileType transition available to be generated and the for loop  below won't
    #   change this value if there wasn't a possible transition available.
    chosenTileType = None

    lTargetTileTypeTransitionProbs = MCData._Get_Component("LIST:MCData")[iChunkLayer][lTileRelation[1]][lTileRelation[0]][iPrevTileType]

    #Here we iterate through each tileType that is available to transition to from the iPrevTileType on the iChunkLayer layer.
    for tileType in xrange(len(lTargetTileTypeTransitionProbs)):

        #Here we check to see if this targetTileType's transition probability will
        #   make the totalProbability greater than the randomProbability (assuming it was smaller beforehand.)
        if (randomProbability < totalProbability + lTargetTileTypeTransitionProbs[tileType]._Get_Count())  \
           and (randomProbability >= totalProbability):

            #So since we found the targetTileType that we're generating,
            #   we'll save that tileType and break out of this loop.
            chosenTileType = tileType
            break

        else:
            #We haven't found the tileType yet, so we're going to
            #   update the totalProbability and move on to the next
            #   trasition.
            totalProbability += lTargetTileTypeTransitionProbs[tileType]._Get_Count()
            

    #Return the tileType that was picked.
    return chosenTileType


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



def Save_Mouse_Tile_Pos(dEntities):
    """This is for the tile editor and is called when the user presses the left mouse button.
    And what it will do is essentially save the tile position where the mouse is. That allows
    another system function to know which tilessssss the user selected for altering."""

    position = sf.Mouse.get_position(config.window)

    if position[0] >= config.windowView.viewport.left     \
       and position[1] >= config.windowView.viewport.top:
        position = config.window.convert_coords(position[0], position[1], config.windowView)

        xOffset = position[0] % config.TILE_SIZE
        yOffset = position[1] % config.TILE_SIZE
        
        dEntities["StartPos"]._Get_Component("POS:MouseTilePos")._Set_Position([int((position[0]-xOffset) / config.TILE_SIZE),  \
                                                                                int((position[1]-yOffset) / config.TILE_SIZE)])

    #If it turns out that the mouse doesn't fit within the window, we can
    #   just set the position to -1,-1. But that means we have to check for
    #   that later when we go to find the end position.
    else:

        dEntities["StartPos"]._Get_Component("POS:MouseTilePos")._Set_Position([-1,-1])

        print "The starting position for the tile altering wasn't within the screen."

    return "NULL,NULL"

def Alter_Selected_Tile_Area(dEntities):
    """This is the second part of the Save_Mouse_Tile_Pos() system func and its purpose
    is to make a list of the tiles that are within the box the user selected. Then it
    will give that list to Alter_Tiles() and consequently alter the selected area accordingly."""

    #This prevents the program from altering tiles when the starting position is found to be outside of the window.
    if dEntities["StartPos"]._Get_Component("POS:MouseTilePos")._Get_Position() != [-1,-1]:

        startTileX = dEntities["StartPos"]._Get_Component("POS:MouseTilePos")._Get_X()
        startTileY = dEntities["StartPos"]._Get_Component("POS:MouseTilePos")._Get_Y()

        position = sf.Mouse.get_position(config.window)

        if position[0] >= config.windowView.viewport.left         \
           and position[1] >= config.windowView.viewport.top:
                position = config.window.convert_coords(position[0], position[1], config.windowView)

                offset = position[0] % config.TILE_SIZE
                endTileX = int((position[0]-offset) / config.TILE_SIZE)

                offset = position[1] % config.TILE_SIZE
                endTileY = int((position[1]-offset) / config.TILE_SIZE)

                tiles = []
                xStep = None
                yStep = None
                xOffset = 0
                yOffset = 0

                if startTileX > endTileX:
                    xStep = -1
                    xOffset = -1
                else:
                    xStep = 1
                    xOffset = 1

                if startTileY > endTileY:
                    yStep = -1
                    yOffset = -1
                else:
                    yStep = 1
                    yOffset = 1

                for tileX in xrange(startTileX, endTileX+xOffset, xStep):
                    if tileX < (config.windowView.viewport.left + config.windowView.width) // config.TILE_SIZE:
                        for tileY in xrange(startTileY, endTileY+yOffset, yStep):
                            if tileY < (config.windowView.viewport.top + config.windowView.height) // config.TILE_SIZE:
                                tiles.append((tileX, tileY, 1, 1))

                Alter_Tiles({"lTileData":tiles, "ChunkMan":dEntities["ChunkMan"]})

    return "NULL,NULL"
                

def Alter_Tiles(dEntities):

    #Just initializing some variables for the upcoming for loop
    alteredChunks = {}

    chunkDict = dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict")
    worldPos = dEntities["ChunkMan"]._Get_Component("POS:WorldPos")._Get_Position()
    rebuildList = dEntities["ChunkMan"]._Get_Component("LIST:RebuildList")

    #This assumes all elements of listOfTiles are tuples with four integers in each.
    for (x, y, z, newTileType) in dEntities["lTileData"]:

        #print "Tile Altered:", x, y, z, newTileType

        #Fill the variables we're going to be using to find the tile and chunk we're altering.
        #This represents the tile position within the chunk it belongs to
        xTileOffset = x % config.CHUNK_TILES_WIDE
        #This represents the chunk position (of the chunk the tile is inside of) within the window!
        xChunkOffset = int((x-xTileOffset) / config.CHUNK_TILES_WIDE) + worldPos[0]

        yTileOffset = y %config.CHUNK_TILES_HIGH
        yChunkOffset = int((y-yTileOffset) / config.CHUNK_TILES_HIGH) + worldPos[1]

        #print xTileOffset, yTileOffset, xChunkOffset, yChunkOffset

        #Now we're altering the chunk at chunk position ( self._x_World_Chunk_Position + xChunkOffset, self._y_World_Chunk_Position + yChunkOffset )
        chunkDict["%d,%d" % (xChunkOffset, yChunkOffset)]._Get_Component("LIST:Tiles")[yTileOffset][xTileOffset][z]._Set_TileID(newTileType)

        alteredChunks["%d,%d" % (xChunkOffset, yChunkOffset)] = 1

    for chunkPosition in alteredChunks.keys():
        rebuildList._Add(chunkDict[chunkPosition])



def Move_Chunk_Position(dEntities):
    """This will add/remove chunks from our dictionary and is meant to be used when we translate our window across the chunk world (because scrolling.)
    There are chunks assumed to already be active on the screen."""

    xOffset = dEntities["Offset"]._Get_Component("POS:direction")._Get_X()
    yOffset = dEntities["Offset"]._Get_Component("POS:direction")._Get_Y()

    #print "Offsets are %d,%d" % (xOffset, yOffset)
    
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

        xEven = None
        yEven = None

        #These variables are determined before the following for loop because they will otherwise have to be calculated more than once.
        if (chunksInWindow[0] + xOffset) % 2 == 0:
            xEven = True
        else:
            xEven = False

        if (chunksInWindow[1] + yOffset) % 2 == 0:
            yEven = True
        else:
            yEven = False

        #print "Moving the world position!"

        #If we move our world chunk position, then we will essentially need to reset all of the chunk's window positions (that are still on the screen.)
        #And the chunks that move off the screen will remain unaltered in case they return to their original window position (which then it won't need its mesh rebuilt.)
        for i in xrange( worldPos[0] - 1, worldPos[0] + chunksInWindow[0] + 1 ):
            for j in xrange( worldPos[1] - 1, worldPos[1] + chunksInWindow[1] + 1 ):

                #This checks to see if the chunk already exists in our dictionary (it was already inside the window or window buffer.)
                if chunkDict._Get("%d,%d"%(i,j)) != None:

                    pChunk = chunkDict["%d,%d"%(i,j)]

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
                    chunkDict["%d,%d"%(i,j)] = entities.Assemble_Chunk( "%s,%s" % (i, j),       \
                                                                          "Chunk",              \
                                                                          random.choice(chunkDict.values()),        \
                                                                          {"WorldPos":"%d,%d"%(i,j),                \
                                                                           "WindowPos":str(i - worldPos[0])+","+str(j - worldPos[1])} )


                    pChunk = chunkDict["%d,%d"%(i,j)]

                    loadList._Add(pChunk)
                    #Schedule an old chunk to be unloaded and then removed from the chunk dictionary

                    #Find the middle chunk position inbetween the previous and the next world chunk position.
                    midChunkX = worldPos[0] - xOffset + (chunksInWindow[0] + xOffset)//2   #Note that the division operator will round down when the result isn't a whole number.
                    midChunkY = worldPos[1] - yOffset + (chunksInWindow[1] + yOffset)//2

                    #These if statements make it possible to use this method when there are an even or odd amount of chunks in the window.
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
                    pChunk = chunkDict["%d,%d"%(p,q)]

                    unloadList._Add(pChunk)

    return "NULL,NULL"

def Update(dEntities):
    """This will initiate all of the different updates that need done for
    the Chunk Manager Entity."""
    
    Update_Load_List({"LoadList":dEntities["ChunkMan"]._Get_Component("LIST:LoadList"),                 \
                      "ChunkDataDir":dEntities["ChunkMan"]._Get_Component("MISC:ChunkDataDir")})

    #This checks to see if the ChunkManager doesn't belong to a EntityManager. If it does belong to
    #   an EntityManager, then we'll need to add the tiles to the Collision space of the ENtityManager.
    if dEntities.get("EntityMan",None) == None:
        
        Update_Rebuild_List({"RebuildList":dEntities["ChunkMan"]._Get_Component("LIST:RebuildList"),    \
                            "FlagList":dEntities["ChunkMan"]._Get_Component("LIST:FlagList"),           \
                            "VisibilityUpdate":dEntities["ChunkMan"]._Get_Component("FLAG:VisibilityUpdate")})

    else:

        Update_Rebuild_List({"RebuildList":dEntities["ChunkMan"]._Get_Component("LIST:RebuildList"),            \
                            "FlagList":dEntities["ChunkMan"]._Get_Component("LIST:FlagList"),                   \
                            "VisibilityUpdate":dEntities["ChunkMan"]._Get_Component("FLAG:VisibilityUpdate"),   \
                             "CollisionSpace":dEntities["EntityMan"]._Get_Component("CSPACE:EntityPool")})

    Update_Unload_List({"UnloadList":dEntities["ChunkMan"]._Get_Component("LIST:UnloadList"),     \
                       "ChunkDict":dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict"),        \
                        "ChunkDataDir":dEntities["ChunkMan"]._Get_Component("MISC:ChunkDataDir")})

    #This will be entered when the rebuild list rebuilds its first chunk.
    if dEntities["ChunkMan"]._Get_Component("FLAG:VisibilityUpdate")._Get_Flag():

        Update_Flag_List({"FlagList":dEntities["ChunkMan"]._Get_Component("LIST:FlagList")})

        #Update the render list if the camera's Position has changed
        Update_Render_List({"ChunkDict":dEntities["ChunkMan"]._Get_Component("DICT:ChunkDict"),         \
                           "WorldPos":dEntities["ChunkMan"]._Get_Component("POS:WorldPos"),             \
                           "ChunksInWind":dEntities["ChunkMan"]._Get_Component("POS:ChunksInWind"),     \
                           "RenderList":dEntities["ChunkMan"]._Get_Component("RLIST:RenderList")})

        dEntities["ChunkMan"]._Get_Component("FLAG:VisibilityUpdate")._Set_Flag(False)

    return "NULL,NULL"


def Update_Load_List(dEntities):
    """This will signal chunks to load its data from their text files. Don't confuse this for updating the meshes of the chunks."""

    for iChunk in xrange(len(dEntities["LoadList"])-1,-1,-1):

        #Checks to see if the chunk has been loaded yet
        if dEntities["LoadList"][iChunk]._Get_Component("FLAG:IsLoaded")._Get_Flag() == False:

            #print "Chunk being loaded", dEntities["LoadList"][iChunk]._Get_Component("POS:WorldPos")._Get_Position()

            #Loads the tile data from its file
            Load_Data({"chunk":dEntities["LoadList"][iChunk],
                       "ChunkDataDir":dEntities["ChunkDataDir"]})
            dEntities["LoadList"][iChunk]._Get_Component("FLAG:IsLoaded")._Set_Flag(True)

            dEntities["LoadList"]._Remove(iChunk)

def Update_Rebuild_List(dEntities):
    """If a chunk has been updated and added to the rebuild_List. Then we will be signaling it to rebuild its mesh here. I also took out the section that
    was trying to optimize the render calls. But then I realized that in a 2d world, chunks can't really be occluded by other chunks (was thinking in 3d.)"""

    iNumberOfChunksRebuilt = 0

    for iChunk in xrange(len(dEntities["RebuildList"])-1,-1,-1):

        #Checking to see if the chunk has been loaded yet
        if iNumberOfChunksRebuilt < 5       \
           and dEntities["RebuildList"][iChunk]._Get_Component("FLAG:IsLoaded")._Get_Flag():

            if dEntities.get("CollisionSpace",None) == None:

                Build_Meshes({"chunk":dEntities["RebuildList"][iChunk]})

            else:

                Build_Collidable_Meshes({"chunk":dEntities["RebuildList"][iChunk],  \
                                         "CollisionSpace":dEntities["CollisionSpace"]})

            iNumberOfChunksRebuilt += 1

            #This limits us to doing only one update to this component
            if iNumberOfChunksRebuilt == 1:

                dEntities["VisibilityUpdate"]._Set_Flag(True)

            dEntities["FlagList"]._Add(dEntities["RebuildList"]._Pop(iChunk))  #removes the chunk pointer from the list


def Update_Unload_List(dEntities):
    """Here we will be freeing the memory associated with chunks that are far enough away from the window that we don't care about them anymore.
    So we will pop them from the _chunk_Dict and then save their data to their respective file."""

    for iChunk in xrange(len(dEntities["UnloadList"])-1,-1,-1):

        if dEntities["UnloadList"][iChunk]._Get_Component("FLAG:IsLoaded")._Get_Flag():

            #This will save the contents of our chunk to a file (so we can free our memory.)
            Unload({"chunk":dEntities["UnloadList"][iChunk],
                    "ChunkDataDir":dEntities["ChunkDataDir"]})

            #print dEntities["UnloadList"]._Get(iChunk)._Get_Component(CWORLD_POS)._Get_Position()

            #Now we take the chunk and chunk pointer variables outside of the lists because they aren't needed anymore.
            dEntities["ChunkDict"]._Remove(str(dEntities["UnloadList"][iChunk]._Get_Component("POS:WorldPos")._Get_X())  \
                                           + "," + str(dEntities["UnloadList"][iChunk]._Get_Component("POS:WorldPos")._Get_Y()))
    
            dEntities["UnloadList"]._Remove(iChunk)

def Update_Flag_List(dEntities):
    """The chunks within the flag list have just recently either been loaded or had their tile data altered. So here we will see if those chunks are empty. And if they are,
    we'll just update their flags."""

    #This computation is quite small, so I haven't limited the updates.
    for iChunk in xrange(len(dEntities["FlagList"])-1,-1,-1):
        #This will tell the chunk to determine if it is empty or not
        Flag_Update({"chunk":dEntities["FlagList"][iChunk]})

        #print "updating flagList!"

        #This removes the pointer from our flag update list.
        dEntities["FlagList"]._Remove(iChunk)

def Update_Render_List(dEntities):
    """Depending on where window is in the world and which chunks are renderable. We will determine which chunks are going to be rendered
    next time rendering occurs."""

    dEntities["RenderList"]._Clear()

    #print dEntities["ChunkDict"]

    #print "These are the world positions of the chunks that are in the render list!"

    #Only the chunks within the window are applicable
    #This will iterate through all of the chunks inside the window at the moment.
    for i in xrange( dEntities["WorldPos"]._Get_X(), dEntities["WorldPos"]._Get_X() + dEntities["ChunksInWind"]._Get_X() ):
        for j in xrange( dEntities["WorldPos"]._Get_Y(), dEntities["WorldPos"]._Get_Y() + dEntities["ChunksInWind"]._Get_Y() ):

            #Check to see if the chunk is loaded and not empty!
            if dEntities["ChunkDict"]["%d,%d"%(i,j)]._Get_Component("FLAG:IsLoaded")._Get_Flag() \
               and not dEntities["ChunkDict"]["%d,%d"%(i,j)]._Get_Component("FLAG:IsEmpty")._Get_Flag():

                #print "A chunk is being added to the render List!"

                pChunk = dEntities["ChunkDict"]["%d,%d"%(i,j)]

                #Put the chunk pointer into the render list!
                dEntities["RenderList"]._Add(pChunk)


def Load_Data(dEntities):
    """From the data within the chunk's file, we then give this list of lists as an argument for the Chunk's _Load_Data().
    So from here we'll update the self._tiles list of lists with a list of lists of similar size (the data.)"""

    fileName = ""
    
    fileName = dEntities["ChunkDataDir"]._Get_Storage()   \
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
        #print fileName, "data file wasn't found, so the chunk will be filled in as though empty."

        #If the file doesn't exist, then we can just fill our chunk with transparent tiles!
        for row in xrange(config.CHUNK_TILES_HIGH):
            for col in xrange(config.CHUNK_TILES_WIDE):
                for depth in xrange(config.CHUNK_LAYERS):

                    tiles[row][col][depth]._Set_TileID(0)

def Unload(dEntities):
    """This is where we'll be saving the contents of a chunk to a file."""

    #print "unloading chunk", str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_X()) \
    #                + " " + str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_Y())

    #print dEntities["chunk"]._Get_Component("FLAG:IsEmpty")._Get_Flag()

    fileName = dEntities["ChunkDataDir"]._Get_Storage()   \
                + str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_X()) \
                + " " + str(dEntities["chunk"]._Get_Component("POS:WorldPos")._Get_Y()) + ".txt"

    #print "unloading chunk to %s"%fileName

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

    #print windowPos
    
    #Handles the building of the tiles within the chunk
    for j in xrange(config.VIEW_TILE_HEIGHT):
        for i in xrange(config.VIEW_TILE_WIDTH):
            #This assumes that depth 0 is the very front of the screen.
            for k in xrange(config.CHUNK_LAYERS):

                if dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_Is_Active():

                    #Calculates the position inside of our window where the tile will be placed
                    tileXPos = i*config.TILE_SIZE + windowPos[0]*config.CHUNK_TILES_WIDE*config.TILE_SIZE
                    tileYPos = j*config.TILE_SIZE + windowPos[1]*config.CHUNK_TILES_HIGH*config.TILE_SIZE

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
                    #print "ActiveTile!", tileXPos, tileYPos
                    #If this tile isn't partially see-through, then all tiles behind it are occluded and we don't need to add them to their meshes.
                    if dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_Is_Transparent() != True:
                        #This is confirmed to correctly break out of ONLY the CHUNK_LAYERS loop and still allow the other loops to continue.
                        break




def Build_Collidable_Meshes(dEntities):
    """We create a mesh here using a VertexArray for a chunk that's on the screen. This only is meant to be for chunk's in relation to their position on the screen.
    Chunks off the screen don't need to have their meshes updated for no reason, but they can still have their data loaded before getting onto the screen."""
    #Makes sure that we have an empty vertex array to add to

    dEntities["chunk"]._Get_Component("MESH:0")._Clear_Meshes()

    #Here we'll iterate through each shape and remove it from the Pymunk space.
    for cShape in dEntities["chunk"]._Get_All_Components("CSHAPE"):

        dEntities["CollisionSpace"]._Remove_Shape(cShape._Get_Body(), cShape._Get_Shape())

    #Here we must reset all of the collision shapes within this entitiy
    #   (because they're being moved to a different spot.)
    dEntities["chunk"]._Remove_All_Components("CSHAPE")

    windowPos = dEntities["chunk"]._Get_Component("POS:WindowPos")._Get_Position()

    windowPos[0] = int(windowPos[0])
    windowPos[1] = int(windowPos[1])

    #print windowPos
    
    #Handles the building of the tiles within the chunk
    for j in xrange(config.VIEW_TILE_HEIGHT):
        for i in xrange(config.VIEW_TILE_WIDTH):
            #This assumes that depth 0 is the very front of the screen.
            for k in xrange(config.CHUNK_LAYERS):

                if dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_Is_Active():

                    #Calculates the position inside of our window where the tile will be placed
                    tileXPos = i*config.TILE_SIZE + windowPos[0]*config.CHUNK_TILES_WIDE*config.TILE_SIZE
                    tileYPos = j*config.TILE_SIZE + windowPos[1]*config.CHUNK_TILES_HIGH*config.TILE_SIZE

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

                    #Currently only the tiles of a specific layer are put into the collision space.
                    if k == 1:

                        cBoxComponent = components.Collision_Box({"componentID":"%d,%d,%d"%(j,i,k),                   \
                                                                    "dependentComponentName":"TILE:%d,%d,%d"%(j,i,k),   \
                                                                    "collisionType":"static",                                   \
                                                                    "staticBody":dEntities["CollisionSpace"]._Get_Static_Body(),     \
                                                                    "xOffset":tileXPos,                                              \
                                                                    "yOffset":tileYPos,                                              \
                                                                    "width":config.TILE_SIZE,                                   \
                                                                    "height":config.TILE_SIZE})

                        dEntities["CollisionSpace"]._Add_Shape(cBoxComponent._Get_Body(), cBoxComponent._Get_Shape())


                        dEntities["chunk"]._Add_Component(cBoxComponent)
                    
                    #print "ActiveTile!", tileXPos, tileYPo
                    #If this tile isn't partially see-through, then all tiles behind it are occluded and we don't need to add them to their meshes.
                    if dEntities["chunk"]._Get_Component("LIST:Tiles")[j][i][k]._Get_Is_Transparent() != True:
                        #This is confirmed to correctly break out of ONLY the CHUNK_LAYERS loop and still allow the other loops to continue.
                        break
