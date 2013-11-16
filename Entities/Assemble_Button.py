from Entity import Entity
from ClassRetrieval import getClass

def Assemble_Button(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This assembles a box with text in it! And sets up some other
    components that'll store important information we might need later."""
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    entity._Add_Component(getClass("Box")({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height']}))
    entity._Add_Component(getClass("Text_Line")({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height'], 'text': attribDict['text'], 'font': attribDict['Font']["Asman"]}))
    entity._Add_Component(getClass("Flag")({'componentID': '0', 'flag': False}))

    return entity
