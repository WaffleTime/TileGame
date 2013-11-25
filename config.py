#These are Global variables for the program

FRAME_RATE = 42

LOADING_FRAME_RATE = 2


#These two vars will contain two sfml objects that until recently
#   were just stored within the main.py's main().
#   They are stored here now, because the system functions for altering the tiles
#   need to be able to query for the mouse's locations
window = None
windowView = None

FOREGROUND_TILE_TYPES = 5
GROUND_TILE_TYPES = 15
BACKGROUND_TILE_TYPES = 5

TILE_XRELATION_MIN = -8
TILE_XRELATION_MAX = 8
TILE_YRELATION_MIN = -6
TILE_YRELATION_MAX = 6

VIEW_TILE_WIDTH = 16      #Tiles along the x-axis of the visible screen
VIEW_TILE_HEIGHT = 11     #Tiles along the y-axis of the visible screen
TILE_SIZE = 32              #The original tile size that isn't altered (for x- and y-axis)
CHUNK_TILES_WIDE = 16               #Tiles per chunk x-axis
CHUNK_TILES_HIGH = 11               #Tiles per chunk x-axis
CHUNK_LAYERS = 3
TILE_ATLAS_SIZE = 10        #Tiles per atlas (for both the x- and y-axis)

#These will be altered at the beginning of each state to be consistant with the
#   window's size.
Tile_Width = 32
Tile_Height = 32

#The View denotes the size of the user's screen and what it can view inside of the RenderWindow (the RenderWindow is bigger than the view.)
WINDOW_WIDTH = 1024           #Pixels alongthe x-axis of the visible screen
WINDOW_HEIGHT = 704           #Pixels along the y-axis of the visible screen

Saved_Game_Directory = ""

Map_Data_Directory = ""

#Note that the window and view dimensions are dependent on the CHUNK_SIZE/TILE_SIZE.
#This is because the window is going to be the view's size with an extra chunk added to each dimension (x-/y-axis.)
#But if the view's dimensions aren't divisible by the CHUNK_SIZE*TILE_SIZE, then the partially used chunk (that isn't fully covered by the view) will be counted as part of the view's dimensions.
#So then we can have up to 1.999 extra chunks around our window depending on configuration for VIEW_TILE_WIDTH/VIEW_TILE_WIDTH/VIEW_WIDTH/VIEW_HEIGHT and the CHUNK_SIZE/TILE_SIZE.
#Check out Master_Control.__init__() to see how the window's height/width are calculated (they use the globals above.)

#Also note that there can be a single chunk used for the View (or part of one) with the current setup. So then the total amount of chunks that will be in memory would be 16.
#And there is theoretically no limits on how many chunks can be used for the view/window/buffer. But obviously there will be a limit due to performance loss and memory issues at some point.

#The current configuration for the view and window make use of 2x2 (4) chunks in the view, 3x3 (9) chunks in the window and 5x5 (25) chunks in memory (which includes the exterior chunks.)

