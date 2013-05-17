import sfml as sf

class Asset_Manager(object):

    #These four dictionaries will store the SFML objects that are currently in use
    #in the program.
    dFonts = {}
    dTextures = {}
    dSounds = {}
    dMusics = {}

    dFileNames = {'Asman': 'ASMAN.ttf'}

    @staticmethod
    def _Empty_Assets():
        """This essentially will be used at the beginning of each state so that there aren't
        any unnecessary assets in the dictionaries from the last state."""
        Asset_Manager.dFonts.clear()
        Asset_Manager.dTextures.clear()
        Asset_Manager.dSounds.clear()
        Asset_Manager.dMusics.clear()

    @staticmethod
    def _Get_Font(sName):
        """This is for retrieving a pointer to a specific Font object in our dictionary.
        Input: The name of the font's actual file (string.)
        Output: An SFML Font object that was requested."""

        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dFonts.get(sName, None) != None:
            
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dFonts[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            Asset_Manager.dFonts[sName] = sf.Font.load_from_file('Resources/Fonts/'+Asset_Manager.dFileNames[sName])

    @staticmethod
    def _Get_Texture(sName):
        
        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dTextures.get(sName, None) != None:
            
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dTextures[sName]
        else:
            #We must create a new SFML Texture object while using the sFileName to load in a font.
            Asset_Manager.dTextures[sName] = sf.Texture.load_from_file('Resources/Textures/'+Asset_Manager.dFileNames[sName])       

    @staticmethod
    def _Get_Sound(sName):
        """A sound is assumed to be a lot shorter than music and it will be loaded into memory unlike the music (which is streamed.)"""

        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dSounds.get(sName, None) != None:
            
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dSounds[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            Asset_Managers.dSounds[sName] = sf.Sound.load_from_file('Resources/Sounds/'+Asset_Manager.dFileNames[sName])

    def _Get_Music(sName):
        """The Music object that is returned will stream the music as it plays."""

        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dMusics.get(sName, None) != None:
            
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dMusics[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            Asset_Manager.dMusics[sName] = sf.Music.open_from_file('Resources/Musics/'+Asset_Manager.dFileNames[sName])
