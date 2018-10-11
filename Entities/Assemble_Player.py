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
                                                      "static":"UPRIGHT",                               \
                                                      "mass":attribDict["mass"],                        \
                                                      "height":attribDict["FrameHeight"],               \
                                                      "xOffset":lWindPos[0],                            \
                                                      "yOffset":lWindPos[1],                            \
                                                      "CollisionShape":attribDict["CollisionBody"]["body"]}))

    """
    entity._Add_Component(getClass("Tile_Collision_Body")({"componentID":"anchor",                          \
                                                           "dependentComponentID":None,                     \
                                                           "width":int(attribDict["FrameWidth"]),                \
                                                           "height":int(attribDict["FrameHeight"]),              \
                                                           "xOffset":int(lWindPos[0]),                           \
                                                           "yOffset":int(lWindPos[1]),                           \
                                                           "friction":0.0,                                  \
                                                           "staticBody":pymunk.Body(pymunk.inf, pymunk.inf)}))
    
    entity._Add_Component(getClass("Collision_Constraint")({"componentID":"anchor",                         \
                                                            "type":"gearJoint",                             \
                                                            "body1":entity._Get_Component("CBODY:main"),    \
                                                            "body2":entity._Get_Component("CTILEBODY:anchor"),  \
                                                            "phase":"0.0",                                    \
                                                            "ratio":"0.0"}))
    """

    return entity
