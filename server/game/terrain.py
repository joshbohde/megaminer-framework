from mappableObject import *

class Terrain(MappableObject):
    def __init__(self, game, x, y, z):
        MappableObject.__init__(self, game, x, y, z)
        self.blockMove = False
        self.blockBuild = False

    def toList(self):
        list = MappableObject.toList(self)
        list.extend([1*self.blockMove, 1*self.blockBuild])
        return list

