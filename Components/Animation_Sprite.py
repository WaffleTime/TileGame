from component import Component

class Animation_Sprite(Component):
    #This unlike the Animated_Sprite is a one-shot deal. There will be a varying time until completion (because of differring delays and textureStrip sizes,) but
    #this sprite when triggered will become active (at inactive there isn't an image at all) and render one big animation before becoming inactive again.
    #The idea behind it is that it will be able to play a pretty flexible animation because of the fact that it has no limits on the frames horizontally AND vertically.
    def __init__(self, dData):   #sComponentID, textureGrid, fDelay, iFrameWidth, iFrameHeight, iFramesWide, iFramesHigh):
        Component.__init__(self, "ANIMATION:%s"%(dData['componentID']), True, 2)

        #This animation starts off as inactive and will await a trigger from a system function
        self._bActive = False

        #This will denote the time in-between each frame of the animation in the textureGrid.
        self._fDelay = dData['delay']

        #This will tell us when it is time to update the frame.
        self._fAnim_Time = 0.0

        #The current frame on the texture grid (top-left)
        self._iCurrent_Frame = [0,0]

        #The texture grid details
        self._iFrame_Width = dData['frameWidth']
        self._iFrame_Height = dData['frameHeight']
        self._iFrames_Wide = dData['framesWide']
        self._iFrames_High = dData['framesHigh']

        #This holds the texture for the animation!
        self._Animation_Sprite = sf.Sprite(dData['Texture'][0])

        self._Animation_Sprite.set_texture_rect(sf.IntRect(0,0,self._iFrame_Width, self._iFrame_Height))

    def _Activate(self):
        """This will trigger the animation to be played once."""
        self._bActive = True

    def _Deactivate(self):
        """This will either halt the animation or make the last frame invisible"""
        self._bActive = False

        #Reload the variables for another activation!
        self._fAnim_Time = 0.0
        self._iCurrent_Frame = [0,0]
        self._Update_Frame()

    def _Update_Frame(self):
        """This simply will be used to update the frame of the animation within the SFML sprite based off of the data in this class."""
        self._Animation_Sprite.set_texture_rect(IntRect(self._iCurrent_Frame[0]*self._iFrame_Width,     \
                                                        self._iCurrent_Frame[1]*self._iFrame_Height,    \
                                                        self._iFrame_Width,                             \
                                                        self._iFrame_Height))

    def _Update(self, timeElapsed):

        if self._bActive:

            #Check to see if the time counter won't reach the end of the animation this update.
            if self._fAnim_Time + timeElapsed < self._iFrame_Width*self._iFrame_Height*self._fDelay:
                #We update our timecounter variable!
                self._fAnim_Time += timeElapsed

                #Check to see if the time counter has passed the delay between the last and upcoming frame update.
                if self._fAnim_Time >= self._fDelay*(self._iCurrent_Frame[1]*self._iFrames_Wide+self._iCurrent_Frame[0]+1): #The +1 will make us check to see if we've reached the NEXT update.
                    #Check to see if we were at the end of the current row last time.
                    if self._iCurrent_Frame[0] + 1 % self._iFrames_Wide:
                        self._iCurrent_Frame[0] = 0

                        if self._iCurrent_Frame[1] + 1 % self._iFrames_High:
                            #The animation is over in terms of the frames...
                            #The game shouldn't get to this point yet, but this'll be here just in case.
                            self._Deactivate()
                            print "The Animation_Sprite component should be deactivating based off of the time counter, not when the frames reach its end!"

                        else:
                            self._iCurrent_Frame[1] += 1

                    else:
                        self._iCurrent_Frame[0] += 1

                    #This will update the frame based off of the information we just altered.
                    self._Update_Frame()

            else:
                #The animation is over in term of the time...
                self._Deactivate()

    def _Render(self, renderWindow):

        renderWindow.draw(self._Animation_Sprite)
