import components

from Entity import Entity

def Assemble_Player(sEntityName, sEntityType, iDrawPriority, attribDict):
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    entity._Add_Component(components.Animated_Sprite({"componentID":"main",                      \
                                                      "FrameWidth":attribDict["FrameWidth"],     \
                                                      "FrameHeight":attribDict["FrameHeight"],   \
                                                      "Delay":attribDict["Delay"],               \
                                                      "WindPos":attribDict["WindPos"],           \
                                                      "Texture":attribDict["Texture"]}))

    lWindPos = attribDict["WindPos"].split(",")

    print lWindPos

    entity._Add_Component(components.Position({"componentID":"LastPos",     \
                                               "positionX":lWindPos[0],     \
                                               "positionY":lWindPos[1]}))

    

    entity._Add_Component(components.Collision_Box({"componentID":"main",                             \
                                                    "dependentComponentName":"STATE_ANIMATIONS:main", \
                                                    "collisionType":"freeMoving",                     \
                                                    "xOffset":int(lWindPos[0]),  \
                                                    "yOffset":int(lWindPos[1]), \
                                                    "width":attribDict["FrameWidth"],        \
                                                    "height":attribDict["FrameHeight"],      \
                                                    "mass":attribDict["mass"]}))

    return entity
