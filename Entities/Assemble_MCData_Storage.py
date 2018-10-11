from ClassRetrieval import getClass
from Entity import Entity
import config

def Assemble_MCData_Storage(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This is for storing the Markov Chain data for the maps made in the tile editor.
    This essentially is just temporary storage until the map is fully iterated over. Then
    this data will have to be saved to a number of xml files (one for each tile relation
    that will be compatible.)"""

    #This mostly should store a List of Lists of Lists of Lists. The first depth is the layer
    #   that the target tile exists on. The second depth is the tile relation.
    #   The third depth is the relative tile's tile type (on the GROUND layer.) And
    #   the last depth is the target tile's tile type (on the layer specified by the first depth.)

    #So I'm thinking that some more reasonable numbers may look like 8*6*25*25 (30000.)
    #   Since that number is still much larger than the amount of tiles we have loaded in memory at
    #   more points in time (6912,) that's probably what I'm going to shoot for at the most.
    #Note that those numbers are only for a single layer (which there are three of currently.)
    #   So I'm going to figure out the minimum number of tile types that should be available
    #   for the generation. Then all the rest of the tile types would have to be obtained through
    #   chests or crafting.

    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    List = getClass("List")
    Counter = getClass("Counter")
	
    #This will be what stores the Markov Chain data for the map generation.
    #   But after the data is all gathered and converted, it will be saved to
    #   some xml files.
    MCData = List({"componentID":"MCData"})

    for layer in xrange(config.CHUNK_LAYERS):

        tileLayer = List({"componentID":"TileLayer%d"%layer})

        for y in xrange(config.TILE_YRELATION_MIN,config.TILE_YRELATION_MAX+1):
            
            yRelation = List({"componentID":"YRelation%d"%(y)})
            
            for x in xrange(config.TILE_XRELATION_MIN,config.TILE_XRELATION_MAX+1):

                if y == 0 and x == 0:
                    continue
                
                xRelation = List({"componentID":"XRelation%d"%(x)})

                for r in xrange(config.GROUND_TILE_TYPES):

                    relativeTile = List({"componentID":"RelativeTileType%d"%r})

                    if layer == 0:

                        for t in xrange(config.FOREGROUND_TILE_TYPES):

                            relativeTile._Add(Counter({"componentID":"TargetTileType%d"%t}))

                    if layer == 1:

                        for t in xrange(config.GROUND_TILE_TYPES):

                            relativeTile._Add(Counter({"componentID":"TargetTileType%d"%t}))

                    if layer == 2:

                        for t in xrange(config.BACKGROUND_TILE_TYPES):

                            relativeTile._Add(Counter({"componentID":"TargetTileType%d"%t}))

                    xRelation._Add(relativeTile)

                yRelation._Add(xRelation)

            tileLayer._Add(yRelation)

        MCData._Add(tileLayer)

    entity._Add_Component(MCData)

    return entity
                
