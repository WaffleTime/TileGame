import sfml as sf
from tileEngine import Chunk_Manager
import editorConfig as config

#Global Variables
window_View = None
#Holds the Chunk_Manager instance
Chunker = None
selected_Layer = 1
selected_Tile_Type = 0

startTileX = None
startTileY = None

window_Width = None
window_Height = None

move_Flag = False
tile_Update_Flag = False

def init():
    global window_View, window_Width, window_Height

    #Convert the #of chunks into pixel lengths and use that as the window dimensions
    window = sf.RenderWindow( sf.VideoMode(config.WINDOW_WIDTH , config.WINDOW_HEIGHT), "Mapi!" )
    window.clear(sf.Color(0,0,0))     #Make background black

    window.framerate_limit = 50   #Just doubled the game update rate

    window_View = sf.View()

    window_View.reset( (0, \
                0, \
                config.WINDOW_WIDTH, \
                config.WINDOW_HEIGHT) )
    return window


def Handle_Input(window):
    """This will handle the user's input for the editor!"""
    global move_Flag, tile_Update_Flag, select_Flag, startTileX, startTileY, selected_Layer, selected_Tile_Type, window_View;
    if (sf.Keyboard.is_key_pressed(sf.Keyboard.R_BRACKET)):

        if not select_Flag:
            selected_Tile_Type += 1

            print "Your selected_Tile_Type is now", selected_Tile_Type

            select_Flag = True

    elif (sf.Keyboard.is_key_pressed(sf.Keyboard.L_BRACKET)):

        if not select_Flag:

            selected_Tile_Type -= 1
            
            print "Your selected_Tile_Type is now", selected_Tile_Type

            select_Flag = True

    elif (sf.Keyboard.is_key_pressed(sf.Keyboard.BACK_SLASH)):

        if not select_Flag:
            
            if selected_Layer == 0:
                selected_Layer = 1
                
            else:
                selected_Layer = 0

            print "Your selected layer is now", selected_Layer

            select_Flag = True

    else:
        select_Flag = False
    if (sf.Keyboard.is_key_pressed(sf.Keyboard.T)):

        finished = False
        while not finished:
            try:
                selected_Tile_Type = input("Enter a tile ID: ")

                if selected_Tile_Type < 0 or selected_Tile_Type > config.TILE_ATLAS_SIZE**2:
                    raise()
                
                finished = True
            except Exception:
                print "Invalid tile ID!"

    elif (sf.Keyboard.is_key_pressed(sf.Keyboard.L)):

        finished = False
        while not finished:
            try:
                selected_Layer = input("Enter a layer: ")
                
                if selected_Layer < 0 or selected_Layer > config.CHUNK_LAYERS:
                    raise()
                
                finished = True
            except Exception:
                print "Enter a number between 0 and 1!"


    if (sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT)):
        if not move_Flag:

            Chunker._Move_Chunk_Position(-1,0)
            move_Flag = True

    elif (sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT)):
        if not move_Flag:
            Chunker._Move_Chunk_Position(1,0)
            move_Flag = True


    elif (sf.Keyboard.is_key_pressed(sf.Keyboard.UP)):
        if not move_Flag:
            Chunker._Move_Chunk_Position(0,-1)
            move_Flag = True

    elif (sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN)):
        if not move_Flag:
            Chunker._Move_Chunk_Position(0,1)
            move_Flag = True

    else:
        move_Flag = False

    if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
        if not tile_Update_Flag:
            position = sf.Mouse.get_position(window)

            if position[0] >= window_View.viewport.left:
                if position[1] >= window_View.viewport.top:
                    position = window.convert_coords(position[0], position[1], window_View)

                    offset = position[0] % config.TILE_SIZE
                    startTileX = int((position[0]-offset) / config.TILE_SIZE)

                    offset = position[1] % config.TILE_SIZE

                    startTileY = int((position[1]-offset) / config.TILE_SIZE)

                    tile_Update_Flag = True


    else:

        if tile_Update_Flag:
            #This denotes the time when the user has let off on the mouse (so we then alter the tiles that have been selected.)
            position = sf.Mouse.get_position(window)

            if position[0] >= window_View.viewport.left:
                if position[1] >= window_View.viewport.top:
                    position = window.convert_coords(position[0], position[1], window_View)

                    offset = position[0] % config.TILE_SIZE
                    endTileX = int((position[0]-offset) / config.TILE_SIZE)

                    offset = position[1] % config.TILE_SIZE
                    endTileY = int((position[1]-offset) / config.TILE_SIZE)

                    tiles = []
                    xStep = None
                    yStep = None
                    xOffset = 0
                    yOffset = 0

                    if startTileX > endTileX:
                        xStep = -1
                        xOffset = -1
                    else:
                        xStep = 1
                        xOffset = 1

                    if startTileY > endTileY:
                        yStep = -1
                        yOffset = -1
                    else:
                        yStep = 1
                        yOffset = 1

                    for tileX in xrange(startTileX, endTileX+xOffset, xStep):
                        if tileX < (window_View.viewport.left + window_View.width) // config.TILE_SIZE:   #The 200 represents the space for the current tile
                            for tileY in xrange(startTileY, endTileY+yOffset, yStep):
                                if tileY < (window_View.viewport.top + window_View.height) // config.TILE_SIZE:
                                    tiles.append((tileX, tileY, selected_Layer, selected_Tile_Type))

                    Chunker._Alter_Tiles(tiles)

                    tile_Update_Flag = False

def main():
    global Chunker
    window = init()

    finished = False
    paused = False

    #The second tuple argument won't be accurate if the WINDOW_(WIDTH,HEIGHT) aren't divisible by the following.
    Chunker = Chunk_Manager((0,0), (int((config.WINDOW_WIDTH/config.CHUNK_TILES_WIDE)/config.TILE_SIZE), int((config.WINDOW_HEIGHT/config.CHUNK_TILES_HIGH)/config.TILE_SIZE)))   #The tuples represent the world chunk position and the chunks within the window


    while not finished:
        #This is the event-driven input (if a key is pressed, there will be an event in our mailbox to check out here)
        #and is mostly for inputs that relate to the window.
        for event in window.iter_events():
            if event.type == sf.Event.CLOSED:
                finished = True

            elif event.type == sf.Event.LOST_FOCUS:
                paused = True

            elif event.type == sf.Event.GAINED_FOCUS:
                paused = False

        window.clear(sf.Color.BLACK)

        window.view = window_View

        if not paused:
            Handle_Input(window)

            Chunker._Update()

        Chunker._Render_Chunks(window)

        window.display()

    window.close()


main()
