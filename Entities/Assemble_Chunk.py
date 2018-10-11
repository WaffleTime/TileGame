from ClassRetrieval import getClass
from Entity import Entity
import config

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

    entity._Add_Component(getClass("Mesh")(dMeshData))

    entity._Add_Component(getClass("Position")({"componentID":"WorldPos",    \
                                               "positionX":attribDict['WorldPos'].split(',')[0],    \
                                               "positionY":attribDict['WorldPos'].split(',')[1]}))
    
    entity._Add_Component(getClass("Position")({"componentID":"WindowPos",   \
                                               "positionX":attribDict['WindowPos'].split(',')[0],   \
                                               "positionY":attribDict['WindowPos'].split(',')[1]}))

    entity._Add_Component(getClass("Flag")({"componentID":"IsEmpty", "flag":True}))
    entity._Add_Component(getClass("Flag")({"componentID":"IsLoaded", "flag":False}))

    List = getClass("List")
    Tile = getClass("Tile")

    tileList = List({"componentID":"Tiles"})

    for row in xrange(config.CHUNK_TILES_HIGH):
        #Adds in a list for each row of the tiles
        tileList._Add(List({"componentID":"Tiles"}))
        
        for col in xrange(config.CHUNK_TILES_WIDE):
            #Adds in a list for each col of the tiles
            tileList[row]._Add(List({"componentID":"Tiles"}))
            for depth in xrange(config.CHUNK_LAYERS):
                #Then adds in a tile, for each layer that exists, into
                #   each 2d tile position in this chunk.
                tileList[row][col]._Add(Tile({"componentID":"%d,%d,%d"%(row,col,depth)}) )

    entity._Add_Component(tileList)

    return entity
