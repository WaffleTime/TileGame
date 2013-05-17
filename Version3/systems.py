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

def Load_Chunk_Entities(dEntities):
    """This will load in some Entities for the Chunk_"""
    pass

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


