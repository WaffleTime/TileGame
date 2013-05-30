import os
import sfml as sf

class Asset_Manager(object):

    #These four dictionaries will store the SFML objects that are currently in use
    #in the program.
    dFonts = {}
    dTextures = {}
    dRenderStates = {}
    dSounds = {}
    dMusics = {}

    @staticmethod
    def _Empty_Assets():
        """This essentially will be used at the beginning of each state so that there aren't
        any unnecessary assets in the dictionaries from the last state."""
        Asset_Manager.dFonts.clear()
        Asset_Manager.dTextures.clear()
        Asset_Manager.dRenderStates.clear()
        Asset_Manager.dSounds.clear()
        Asset_Manager.dMusics.clear()


    @staticmethod
    def _Get_Font(sName, sFileName):
        """This is for retrieving a pointer to a specific Font object in our dictionary.
        Input: The name of the font's actual file (string.)
        Output: An SFML Font object that was requested."""

        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dFonts.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dFonts[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            Asset_Manager.dFonts[sName] = sf.Font.load_from_file('Resources/Fonts/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dFonts[sName]

    @staticmethod
    def _Get_Texture(sName, sFileName):
        
        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dTextures.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dTextures[sName]
        else:
            #We must create a new SFML Texture object while using the sFileName to load in a font.
            Asset_Manager.dTextures[sName] = sf.Texture.load_from_file('Resources/Textures/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dTextures[sName]

    @staticmethod
    def _Get_Render_State(sName, sFileName):
        
        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dRenderStates.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dRenderStates[sName]
        else:
            #We must create a new SFML Texture object while using the sFileName to load in a font.
            texture = sf.Texture.load_from_file('Resources/Textures/'+sFileName)

            Asset_Manager.dRenderStates[sName] = sf.RenderStates(sf.BLEND_ALPHA,
                                                                None,
                                                                texture)

            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dRenderStates[sName]

    @staticmethod
    def _Get_Sound(sName, sFileName):
        """A sound is assumed to be a lot shorter than music and it will be loaded into memory unlike the music (which is streamed.)"""

        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dSounds.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dSounds[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            Asset_Managers.dSounds[sName] = sf.Sound.load_from_file('Resources/Sounds/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dSounds[sName]

    @staticmethod
    def _Get_Music(sName, sFileName):
        """The Music object that is returned will stream the music as it plays."""

        #Check to see if that filename is listed in our dictionary already.
        if Asset_Manager.dMusics.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dMusics[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            Asset_Manager.dMusics[sName] = sf.Music.open_from_file('Resources/Musics/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return Asset_Manager.dMusics[sName]
