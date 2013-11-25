import components
from ClassRetrieval import getClass
from Entity import Entity
import pymunk

def Assemble_Player(sEntityName, sEntityType, iDrawPriority, attribDict):
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    entity._Add_Component(getClass("Animated_Sprite")({"componentID":"main",                      \
                                                      "FrameWidth":attribDict["FrameWidth"],     \
                                                      "FrameHeight":attribDict["FrameHeight"],   \
                                                      "Delay":attribDict["Delay"],               \
                                                      "WindPos":attribDict["WindPos"],           \
                                                      "Texture":attribDict["Texture"]}))

    lWindPos = attribDict["WindPos"].split(",")

    #print lWindPos

    entity._Add_Component(getClass("Position")({"componentID":"LastPos",     \
                                                "positionX":lWindPos[0],     \
                                                "positionY":lWindPos[1]}))

    entity._Add_Component(getClass("Collision_Body")({"componentID":"main",                             \
                                                      "dependentComponentID":"STATE_ANIMATIONS:main",   \
                                                      "MomentType":"box",                               \
                                                      "static":"NO",                                    \
                                                      "mass":attribDict["mass"],                        \
                                                      "width":attribDict["FrameWidth"],                 \
                                                      "height":attribDict["FrameHeight"],               \
                                                      "xOffset":lWindPos[0],                            \
                                                      "yOffset":lWindPos[1],                            \
                                                      "CollisionShape":attribDict["CollisionBody"]["body"]}))

    
    entity._Add_Component(getClass("Collision_Body")({"componentID":"angleAnchor",                      \
                                                      "dependentComponentID":None,                      \
                                                      "static":"YES",                                    \
                                                      "height":attribDict["FrameHeight"],               \
                                                      "xOffset":lWindPos[0],                            \
                                                      "yOffset":lWindPos[1],                            \
                                                      "CollisionShape":attribDict["CollisionBody"]["anchor"]}))


    #pymunk.GearJoint(entity._Get_Component("CBODY:angleAnchor")._Get_Body(), entity._Get_Component("CBODY:main")._Get_Body(), 0, 0)


    return entity
