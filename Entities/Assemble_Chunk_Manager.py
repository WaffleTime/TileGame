import components

from Entity import Entity


def Assemble_Chunk_Manager(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This will return an Entity object that contains a list of lists of lists of tiles,
    some world coordinates, the number of chunks in the screen, and all that stuff that is
    needed in order to manager a chunks of tiles (except for the textures, those are already
    taken care of.)"""
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    if attribDict["ChunkDataDir"] == "SavedGame":
        #Notice that the ChunkDataDir is prefixed by the directory that this file is in.
        entity._Add_Component(components.Misc({"componentID":"ChunkDataDir", "storage":os.getcwd()+config.Saved_Game_Directory}))

    elif attribDict["ChunkDataDir"] == "MapEdi":
        #Notice that the ChunkDataDir is prefixed by the directory that this file is in.
        entity._Add_Component(components.Misc({"componentID":"ChunkDataDir", "storage":os.getcwd()+config.Map_Data_Directory}))    

    else:
        #Notice that the ChunkDataDir is prefixed by the directory that this file is in.
        entity._Add_Component(components.Misc({"componentID":"ChunkDataDir", "storage":os.getcwd()+attribDict["ChunkDataDir"]}))

    entity._Add_Component(components.Position({"componentID":"WorldPos", "positionX":attribDict["WorldPos"].split(',')[0], "positionY":attribDict["WorldPos"].split(',')[1]}))
    entity._Add_Component(components.Position({"componentID":"ChunksInWind", "positionX":attribDict["ChunksInWind"].split(",")[0], "positionY":attribDict["ChunksInWind"].split(",")[1]}))
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
