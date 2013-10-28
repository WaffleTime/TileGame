import sfml as sf
import pymunk
import config

class Component(object):
    def __init__(self, sComponentName, bUpdatable, iDrawableType):
        #This is here to adapt to the dictionary of components within the Entity instances.
        #This name will be used as the Key for this component.
        self._sName = sComponentName
        self._bUpdatable = bUpdatable

        #This integer can be either
        #   0, 1, or 2.
        #   0 - Not Drawable
        #   1 - Screen Drawable
        #   2 - View Drawable
        self._iDrawableType = iDrawableType

    def _Get_Name(self):
        """This is primarily used for letting the Entity class determine
        the key for the component instance"""
        return self._sName

    def _Get_Updatable(self):
        """For checking to see if this component is updatable."""
        return self._bUpdatable

    def _Set_Updatable(self, bUpdatable):
        """For the entities that need to change updatable ability."""
        self._bUpdatable = bUpdatable

    def _Get_View_Drawable(self):
        """For checking to see if this component is drawable."""
        return (self._iDrawableType == 2)

    def _Get_Screen_Drawable(self):
        """For checking to see if this component is drawable."""
        return (self._iDrawableType == 1)

    def _Set_Drawable(self, iDrawableType):
        """For the entities that need to change drawable ability."""
        self._iDrawableType = iDrawableType

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


        #Each animation strip gets
        for key in self._dAnimated_Sprites.keys():
            self._dAnimated_Sprites[key][0].set_texture_rect(sf.IntRect(0,0,self._iFrame_Width,self._iFrame_Height))

    def _Activate(self, sStateKey):
        """This will activate a new animation to be played."""
        self._bActive = True

    def _Deactivate(self):
        """This will either halt the animation or make the last frame invisible"""
        self._bActive = False

        #Reload the variables for another activation!
        self._anim_Time = sf.Time(0.0)
        self._iCurrent_Frame = ["DEFAULT",0]
        self._Update_Frame()

    def _Update_Position(self, lPosition):
        """This is for updating the position of the Sprite. It's crucial for when the physics shapes are queryed for the position
        that their dependent components have a method that allows position updates. So this method WILL be redundant throughout the
        drawable (and collidable) components."""

        #print "AnimatedSPrite position being updated from %d,%d!"%(self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].x,self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].y)

        #print "AnimatedSPrite position being updated to %d,%d!"%(lPosition[0],lPosition[1])

        self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].x = lPosition[0]
        
        #The height of the sprite needs to be altered so that the position refers to the top-left corner instead of the
        #   bottom-left corner
        self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].y = lPosition[1]-self._iFrame_Height
        

    def _Update_Frame(self):
        """This simply will be used to update the frame of the animation within the SFML sprite based off of the data in this class."""

        #print int(self._lCurrent_Frame[1])*self._iFrame_Width,     \
                #0,                                                  \
                #self._iFrame_Width,                                 \
                #self._iFrame_Height
        
        self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].set_texture_rect(sf.IntRect(int(self._lCurrent_Frame[1])*self._iFrame_Width,     \
                                                                                        0,                                                  \
                                                                                        self._iFrame_Width,                                 \
                                                                                        self._iFrame_Height))

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
            #print self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].x, self._dAnimated_Sprites[self._lCurrent_Frame[0]][0].y

            renderWindow.draw(self._dAnimated_Sprites[self._lCurrent_Frame[0]][0])

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

class Collision_Space(Component):
    def __init__(self, dData):
        Component.__init__(self, "CSPACE:%s"%(dData['componentID']), True, 0)

        self._cSpace = pymunk.Space()

        self._cSpace.gravity = (float(dData["gravity"][0]),float(dData["gravity"][1]))

    def _Add_Shape(self, cBody, cShape):
        """This is meants for adding in collision bodies into the collision space.
        @param cBody This is a pymunk Body object. It represents an Entity's body."""

        #print "Adding Shape into Collision Space"
        #print cBody, cShape

        #print cBody.position

        if cBody.is_static:
            self._cSpace.add(cShape)

        else:
            self._cSpace.add(cBody, cShape)

    def _Remove_Shape(self, cBody, cShape):
        """This is meant for removing body and shape collision objects out
        of the Collision SPace."""

        self._cSpace.remove(cBody, cShape)

    def _Get_Static_Body(self):
        """This is just for getting a static body for the collision space."""
        return self._cSpace.static_body

    def _Update(self, timeElapsed):
        """This should tell pymunk to step forward in time
        a certain amount.
        @param timeElapsed The timeElapsed is a sf.Time objecct 
            and it will be the same value each time depending on the
            update rate."""

        #This will step the physics for the Collision_Bodys through an update.
        self._cSpace.step(timeElapsed.as_seconds())


class Collision_Body(Component):
    def __init__(self, dData):
        Component.__init__(self, "CBODY:%s"%(dData['componentID']), False, 0)

        mass = None
        inertia = None
        
        if dData["MomentType"] == "static":
            pass

        elif dData["MomentType"] == "circle":
            mass = int(dData["mass"])
            radius = int(dData["radius"])
            inertia = pymunk.moment_for_circle(mass, 0, radius)

        elif dData["MomentType"] == "box":
            mass = int(dData["mass"])
            width = int(dData["width"])
            height = int(dData["height"])

            inertia = pymunk.moment_for_box(mass, width, height)
            
        self._cBody = pymunk.Body(mass, inertia)

    def _Get_Body(self):
        """This is for returning the collision body."""
        return self._cBody



class Collision_Shape(Component):
    def __init__(self, cShape, cBody, dData):
        Component.__init__(self, "CSHAPE:%s"%(dData['componentID']), False, 0)

        self._sDependent_Comp_Name = dData["dependentComponentName"]

        self._cShape = cShape

        self._cBody = cBody

    def _Get_Shape(self):
        """This is for retrieving the collision shape. It's
        important that all Collision Shape components have a method
        with this exact name. It's used by Entity_PQueue to get the shapes
        within Entities and load them into the collision space with their body (_Add_Entity() is
        the method I speak of.)"""

        return self._cShape

    def _Get_Body(self):
        """This is for retrieving the body of the collision shape.
        It's also necessary within the Entity_PQueue._Add_Entity() method.
        @return A Pymunk Body object that is to be connected to the collision shape
            within the collision space."""

        return self._cBody

    def _Get_Dependent_Comp_Name(self):
        """This is for retrieving the name of the component
        that this collision shape affects."""

        return self._sDependent_Comp_Name


class Collision_Box(Collision_Shape):
    def __init__(self, dData):

        cBody = None

        width = int(dData["width"])
        height = int(dData["height"])

        if dData["collisionType"] != "static":

            mass = int(dData["mass"])
            
            inertia = pymunk.moment_for_box(mass, width, height)

            cBody = pymunk.Body(mass, inertia)

        else:
            
            cBody = dData["staticBody"]

        #This assumes that the dData["yOffset"] is with respect to Pysfml's coordante plane.
        cBody.position = (dData["xOffset"], config.WINDOW_HEIGHT-dData["yOffset"]-int(dData["height"]))

        cBox = pymunk.Poly(cBody,                                         \
                           [ (0,height),    \
                             (width,height),     \
                             (width,0),    \
                             (0,0) ],\
                           (0, 0),                                        \
                           False)

        """cBox = pymunk.Poly(cBody,                                         \
                           [ (-width/2,height/2),    \
                             (width/2,height/2),     \
                             (width/2,-height/2),    \
                             (-width/2, -height/2) ],\
                           (0, 0),                                        \
                           False)"""

        #This will load the Collision_Shape up with the Shape and data that it needs.
        Collision_Shape.__init__(self,      \
                                 cBox,      \
                                 cBody,     \
                                 {"componentID":dData["componentID"],     \
                                  "dependentComponentName":dData["dependentComponentName"]})


    
        
class Box(Component):
    def __init__(self, dData):
        Component.__init__(self, "BOX:%s"%(dData['componentID']), False, 1)
        self._box = sf.RectangleShape((int(dData['width']),int(dData['height'])))
        self._box.position = (int(dData['x']),int(dData['y']))
        self._box.fill_color = sf.Color.WHITE
        self._box.outline_color = sf.Color.RED
        self._box.outline_thickness = 3.0

    def _Set_Color(self, fillColor, outlineColor):
        self._box.fill_color = fillColor
        self._box.outline_color = outlineColor

    def _Get_Color(self):
        return self._box.fill_color

    def _Switch_Color(self):
        tmpColor = self._box.fill_color
        self._box.fill_color = self._box.outline_color
        self._box.outline_color = tmpColor

    def _Get_Box(self):
        return self._box

    def _Render(self, renderWindow):
        renderWindow.draw(self._box)


class Text_Line(Component):
    def __init__(self, dData):  # sComponentID, xPos, yPos, width, height, text, font):
        Component.__init__(self, "TEXTLINE:%s"%(dData['componentID']), False, 1)
        self._text = sf.Text(dData['text'], dData['font'])
        self._text.color = sf.Color.BLACK
        self._text.style = sf.Text.UNDERLINED
        self._text.x = int(dData['x']) + int(dData['width']) / 2.0 - self._text.global_bounds.width / 2.0
        self._text.y = int(dData['y']) + int(dData['height']) / 2.0 - self._text.global_bounds.height / 2.0

    def _Render(self, renderWindow):
        
        renderWindow.draw(self._text)

class Tile(Component):
    """Denotes a single tile within a chunk."""
    def __init__( self, dData ):
        Component.__init__(self, "TILE:%s"%(dData['componentID']), False, 0)
        #Tells whether or not the tile is visible or not
        self._is_Active = False

        #Identifies the type of tile that is drawn (denotes tile IDs on the tile_atlas.)
        self._tileID = 0

        self._isTransparanent = True

    def _Get_TileID(self):
        return self._tileID

    def _Set_TileID(self, iTileID):
        self._tileID = iTileID

        self._Set_Is_Active()

    def _Get_Tile_AtlasID(self):
        return self._tile_AtlasID

    def _Set_Is_Active( self ):
        """Automatically determines if the tile is active or not depending on the tile's type."""
        if self._tileID != 0:
            self._is_Active = True
        else:
            self._is_Active = False

    def _Get_Is_Active( self ):
         return self._is_Active

    def _Get_Is_Transparent(self):
        return self._isTransparanent

    def __str__( self ):
        """This is the tile's string representation for when it is saved to a file."""
        offset = self._tileID%10    #This will get the first digit for our tileID

        return str((self._tileID-offset)/10) + str(offset)

class Mesh(Component):
    """This is for drawing with the gpu!"""
    def __init__(self, dData):
        Component.__init__(self, "MESH:%s"%(dData["componentID"]), False, 0)
        self._mesh = [ [] for layer in xrange(config.CHUNK_LAYERS) ]

        #This is for linking this mesh with a texture within the Asset_Manager.
        self._lTileAtlas = []

        for i in xrange(config.CHUNK_LAYERS):
            self._lTileAtlas.append(dData.get("TileAtlas"+str(i), None))

    def _Clear_Meshes(self):
        #Clears the mesh lists
        for i in xrange(len(self._mesh)):
            self._mesh[i] = []

    def _Add_To_Mesh(self, layer, lVertices):
        """This will concatenate a list of Vertices with the Vertex Array for the given layer index."""
        self._mesh[layer] += lVertices

    def _Get_Meshes(self):
        return self._mesh

    def _Render(self, renderWindow):
        """The mesh at the beginning of the mesh list will
        be the mesh drawn on the front."""

        for layer in xrange(config.CHUNK_LAYERS-1, -1, -1):

            #print self._lTileAtlas[layer]

            #This if is meant to prevent a mesh that doesn't have
            #   a tileAtlas from being able to be rendered.
            #   It's partially for debuging and partially for
            #   preventing exceptions.
            if self._lTileAtlas[layer] != None:
                
                renderWindow.draw(self._mesh[layer], sf.QUADS, self._lTileAtlas[layer])


class Render_List(Component):
    """This is meant for containing Chunk Entities."""
    def __init__(self, dData):
        Component.__init__(self, "RLIST:%s"%(dData['componentID']), False, 2)
        #This can also hold entities.
        self._lComponents = []

    def _Add(self, item):
        self._lComponents.append(item)

    def _Clear(self):
        for i in xrange(len(self._lComponents)-1,-1,-1):
            del self._lComponents[i]

    def _Remove(self, indx):
        del self._lComponents[indx]

    def _Pop(self, indx):
        return self._lComponents.pop(indx)

    def __getitem__(self, indx):
        return self._lComponents[indx]

    def __len__(self):
        return len(self._lComponents)

    def _Render(self, renderWindow):

        for i in xrange(len(self._lComponents)):

            self._lComponents[i]._Get_Component("MESH:0")._Render(renderWindow)


class List(Component):
    """This is for containing Components as well as Entities."""
    def __init__(self, dData):
        Component.__init__(self, "LIST:%s"%(dData['componentID']), False, 0)
        #This can also hold entities.
        self._lComponents = []

    def _Add(self, item):
        self._lComponents.append(item)

    def _Clear(self):
        for key in self._lComponents.keys():
            self._lComponents.pop(key)

    def _Remove(self, indx):
        del self._lComponents[indx]

    def _Pop(self, indx):
        return self._lComponents.pop(indx)

    def __getitem__(self, indx):
        return self._lComponents[indx]

    def __setitem__(self, indx, item):
        self._lComponents[indx] = item

    def __str__(self):
        return str(self._lComponents)

    def __len__(self):
        return len(self._lComponents)

class Dictionary(Component):
    """This is for containing Chunks."""
    def __init__(self, dData):
        Component.__init__(self, "DICT:%s"%(dData['componentID']), False, 0)
        #This can also hold entities
        self._dComponents = {}

    def _Add(self, itemName, item):
        self._dComponents[itemName] = item

    def _Remove(self, itemName):
        del self._dComponents[itemName]

    def __getitem__(self, key):
        return self._dComponents.get(key, None)

    def __setitem__(self, key, value):
        self._dComponents[key] = value

    def values(self):
        return self._dComponents.values()

    def __str__(self):
        return str(self._dComponents)

    def _Clear(self):
        del self._lComponents

    def _Get(self, itemName):
        return self._dComponents.get(itemName, None)


class Flag(Component):
    """This is a piece of logic for Buttons and will tell the button's _box object
    to oscillate its color scheme whenever collisions occur with the mouse and the button."""
    def __init__(self, dData):
        Component.__init__(self, "FLAG:%s"%(dData['componentID']), False, 0)
        self._flag = dData['flag']

    def _Set_Flag(self, isActive):
        self._flag = isActive

    def _Get_Flag(self):
        return self._flag


class State(Component):
    def __init__(self, dData):          #sComponentID, sState):
        Component.__init__(self, "STATE:%s"%(dData['componentID']), False, 0)
        self._sState = dData['state']

    def _Get_State(self):
        return self._sState

class Position(Component):
    def __init__(self, dData):
        Component.__init__(self, "POS:%s"%(dData['componentID']), False, 0)
        self._position = [int(dData['positionX']), int(dData['positionY'])]


    def _Get_Position(self):
        return self._position

    def _Get_X(self):
        return self._position[0]

    def _Get_Y(self):
        return self._position[1]

    def _Set_Position(self, position):
        self._position = position

    def _Add_To_X(self, number):
        self._position[0] += number

    def _Add_To_Y(self, number):
        self._position[1] += number

class Counter(Component):
    def __init__(self, dData):
        Component.__init__(self, "COUNT:%s"%(dData['componentID']), False, 0)
        self._counter = 0

    def _Reset_Counter(self):
        self._counter = 0

    def _Set_Counter(self, count):
        self._counter = count

    def _Add(self, number):
        self._counter += number

    def _Increment(self):
        self._counter += 1

    def _Decrement(self):
        #Reject decrements that will make the counter negative.
        if self._counter > 0:
            self._counter -= 1


    def _Get_Count(self):
        return self._counter

class Misc(Component):
    def __init__(self, dData):
        Component.__init__(self, "MISC:%s"%(dData['componentID']), False, 0)
        self._storage = dData['storage']

    def _Set_Storage(self, variable):
        self._storage = variable

    def _Get_Storage(self):
        return self._storage
