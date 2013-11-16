import sfml as sf

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
