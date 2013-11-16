from component import Component

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
