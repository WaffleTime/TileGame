from component import Component
import config
import sfml as sf

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

        #print "rendering mesh"

        for layer in xrange(config.CHUNK_LAYERS-1, -1, -1):

            #print self._lTileAtlas[layer]

            #This if is meant to prevent a mesh that doesn't have
            #   a tileAtlas from being able to be rendered.
            #   It's partially for debuging and partially for
            #   preventing exceptions.
            if self._lTileAtlas[layer] != None:
                
                renderWindow.draw(self._mesh[layer], sf.QUADS, self._lTileAtlas[layer])

