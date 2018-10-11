from Entity import Entity
from ClassRetrieval import getClass

def Assemble_Text_Box(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This assembles a box with text in it!"""
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    #The first argument represents the ID of the component with respect to its type (multiple components of a single type need to have different IDs.)
    entity._Add_Component(getClass("Box")({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height']}))
    entity._Add_Component(getClass("Text_Line")({'componentID': "0", 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height'], 'text': attribDict['text'], 'font': attribDict["Font"]["Asman"]}))

    return entity
