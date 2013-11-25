from component import Component
import sfml as sf
from math import pi

class Animated_Sprite(Component):
    #This will be a sprite that can switch its sprite animation according to the state that the parent Entity is in.
    def __init__(self, dData):      #sComponentID, iFrameWidth, iFrameHeight, dTextureStripData):
        Component.__init__(self, "STATE_ANIMATIONS:%s"%(dData['componentID']), True, 2)

        self._bActive = True

        #This will denote the time in-between each frame of the animation in the textures
        self._fDelay = float(dData['Delay'])

        #This will tell us when it is time to update the frame.
        self._anim_Time = sf.Time(0.0)

        #The current animation is set to its default (which there should be...)
        #   The first item is the animation, the second is the frame.
        self._lCurrent_Frame = ['DEFAULT',0]

        self._iFrame_Width = int(dData['FrameWidth'])
        self._iFrame_Height = int(dData['FrameHeight'])

        self._dAnimated_Sprites = {}


        windPos = dData["WindPos"].split(",")


        for sTextureName in dData["Texture"].keys():
            
            #This holds the textures for the animations!
            #It being in a dictionary allows systems to switch to animations easier.
            #Each sAnimation will have a list of the sprite and some data for flexible lengthed animations to be allowed.
            #The list will include [sprite, iFramesWide]
            ##only the width is needed because this is a one-dimensional strip (I think this is all we need... Unless we're dealing with LARGE frame dimensions...)
            self._dAnimated_Sprites[sTextureName] = [sf.Sprite(dData["Texture"][sTextureName]),     \
                                                     int(dData["Texture"][sTextureName].width)/self._iFrame_Width]

            self._dAnimated_Sprites[sTextureName][0].x = float(windPos[0])
            self._dAnimated_Sprites[sTextureName][0].y = float(windPos[1])

            self._dAnimated_Sprites[sTextureName][0].origin = (self._iFrame_Width/2, self._iFrame_Height/2)

            #print "The sprite's origin is", (self._iFrame_Width/2, self._iFrame_Height/2)


        #Each animation strip gets
        for key in self._dAnimated_Sprites.keys():
            self._dAnimated_Sprites[key][0].set_texture_rect(sf.IntRect(0,0,self._iFrame_Width,self._iFrame_Height))

    def _Activate(self, sStateKey):
        """This will activate a new animation to be played."""
        self._bActive = True

        print "The new animation state is", sStateKey

        #Reload the variables for another activation!
        self._anim_Time = sf.Time(0.0)
        self._lCurrent_Frame = [sStateKey,0]
        self._Update_Frame()

    def _Deactivate(self):
        """This will either halt the animation or make the last frame invisible"""
        self._bActive = False

        #Reload the variables for another activation!
        self._anim_Time = sf.Time(0.0)
        self._lCurrent_Frame = ["DEFAULT",0]
        self._Update_Frame()

    def _Get_State():
        """The rest of the components need to know what state the sprite is in currently. So this will
        return the key of the sprite's state."""
        return self._lCurrent_Frame[0]

    def _Update_Position(self, lPosition, fRotation):
        """This is for updating the position of the Sprite. It's crucial for when the physics shapes are queryed for the position
        that their dependent components have a method that allows position updates. So this method WILL be redundant throughout the
        drawable (and collidable) components."""

        #print "AnimatedSPrite position being updated from %d,%d!"%(self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].x,self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].y)

        #print "AnimatedSPrite position being updated to %d,%d!"%(lPosition[0],lPosition[1])

        sprite = self._dAnimated_Sprites[self._lCurrent_Frame[0]][0]

        sprite.x = lPosition[0]
        
        #The height of the sprite needs to be altered so that the position refers to the top-left corner instead of the
        #   bottom-left corner
        sprite.y = lPosition[1]-self._iFrame_Height

        fRotation = 180 * fRotation / pi

        sprite.rotation = fRotation

        
        

    def _Update_Frame(self):
        """This simply will be used to update the frame of the animation within the SFML sprite based off of the data in this class."""

        #print int(self._lCurrent_Frame[1])*self._iFrame_Width,     \
                #0,                                                  \
                #self._iFrame_Width,                                 \
                #self._iFrame_Height

        if (self._dAnimated_Sprites.get(self._lCurrent_Frame[0], None) != None):
        
            self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].set_texture_rect(sf.IntRect(int(self._lCurrent_Frame[1])*self._iFrame_Width,     \
                                                                                            0,                                                  \
                                                                                            self._iFrame_Width,                                 \
                                                                                            self._iFrame_Height))
        else:
            print "There is no %s animation for %s"%(self._lCurrent_Frame[0], self._Get_Name())

    def _Update(self, timeElapsed):
        """This will update the frame of the animation based off of the timeElapsed and the current time in
        the animation.
        @param timeElapsed """

        if self._bActive:
            
            #print self._anim_Time + timeElapsed, sf.Time(self._dAnimated_Sprites[self._lCurrent_Frame[0]][1]*self._fDelay)

            #Check to see if the time counter will reach the end of the animation this update.
            if self._anim_Time + timeElapsed >= sf.Time((self._dAnimated_Sprites[self._lCurrent_Frame[0]][1])*self._fDelay):

                #Since we reached the end of the animation, we
                #   must rrest the animation time and the frame number.
                self._anim_Time = self._anim_Time + timeElapsed - sf.Time((self._dAnimated_Sprites[self._lCurrent_Frame[0]][1]-1)*self._fDelay)
                
                self._lCurrent_Frame[1] = 0

                #Then we can update the sprite so that
                #   it shows the updated position in the animation.
                self._Update_Frame()

            #Check to see if the animation is due to switch it's frame.
            elif self._anim_Time + timeElapsed >= sf.Time((self._lCurrent_Frame[1]+1)*self._fDelay):

                #We update our timecounter variable!
                self._anim_Time += timeElapsed

                #Else, just update the frame
                self._lCurrent_Frame[1] += 1

                #Then we can update the sprite so that
                #   it shows the updated position in the animation.
                self._Update_Frame()


            else:

                #We update our timecounter variable!
                self._anim_Time += timeElapsed

    def _Render(self, renderWindow):
        """
        @param renderWindow This is SFML's Window object for the program.
        @post the current frame of the animation will be drawn."""

        if self._bActive:

            #print "AnimatedSprite to be rendered"
            #print self._lCurrent_Frame
            #print self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].x, self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].y

            renderWindow.draw(self._dAnimated_Sprites[self._lCurrent_Frame[0]][0])
