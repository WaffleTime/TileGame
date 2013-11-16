from component import Component

class Counter(Component):
    def __init__(self, dData):
        """dData must contain a componentID for identification. But the lowerBound and
        upperBound are optional. The upperBound and lowerBound are included in the bounds
        that are defined by them (the range in math is [lowerBound, upperBound])"""
        Component.__init__(self, "COUNT:%s"%(dData['componentID']), False, 0)

        if ('lowerBound' in dData) \
           and (dData['lowerBound'].isdigit()):
            self._counter = int(dData['lowerBound'])
            self._lowerBound = int(dData['lowerBound'])
        else:
            self._counter = 0
            self._lowerBound = -1

        if 'upperBound' in dData \
           and (dData['upperBound'].isdigit()):
            self._upperBound = int(dData['upperBound'])
        else:
            self._upperBound = -1

    def _Reset_Counter(self):
        self._counter = 0

    def _Set_Counter(self, count):
        withinBounds = True
        
        if (self._lowerBound != -1):
            if (self._lowerBound > count):
                self._counter = self._lowerBound

                withinBounds = False

        if (self._upperBound != -1):
            if (self._upperBound < count):
                self._counter = self._upperBound

                withinBounds = False

        if withinBounds:
            self._counter = count

    def _Add(self, number):
        if (number != -1):
            self._counter += number

    def _Increment(self):
        if (self._counter < self._upperBound):
            self._counter += 1

    def _Decrement(self):
        #Reject decrements that will make the counter negative.
        if (self._counter > 0) and (self._counter > self._lowerBound):
            self._counter -= 1


    def _Get_Count(self):
        return self._counter
