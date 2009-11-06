# -*- python -*-

from library import library

class BaseAI:
    """@brief A basic AI interface.

    This class implements most the code an AI would need to interface with the lower-level game code.
    AIs should extend this class to get a lot of builer-plate code out of the way
    The provided AI class does just that.
    """
    initialized = False
    iteration = 0
    buildings = []
    buildingTypes = []
    portals = []
    terrains = []
    units = []
    unitTypes = []

    def startTurn(self):
        from GameObject import Building
        from GameObject import BuildingType
        from GameObject import Portal
        from GameObject import Terrain
        from GameObject import Unit
        from GameObject import UnitType

        BaseAI.buildings = [Building(library.getBuilding(i)) for i in xrange(library.getBuildingCount())]
        BaseAI.buildingTypes = [BuildingType(library.getBuildingType(i)) for i in xrange(library.getBuildingTypeCount())]
        BaseAI.portals = [Portal(library.getPortal(i)) for i in xrange(library.getPortalCount())]
        BaseAI.terrains = [Terrain(library.getTerrain(i)) for i in xrange(library.getTerrainCount())]
        BaseAI.units = [Unit(library.getUnit(i)) for i in xrange(library.getUnitCount())]
        BaseAI.unitTypes = [UnitType(library.getUnitType(i)) for i in xrange(library.getUnitTypeCount())]

        if not self.initialized:
            self.initialized = True
            self.init()
        BaseAI.iteration += 1;
        return self.run()
    
    @staticmethod
    def maxX():
        return library.getMaxX()

    @staticmethod
    def maxY():
        return library.getMaxY()

    @staticmethod
    def player0Gold0():
        """Player 0's past gold
        """
        return library.getPlayer0Gold0()

    @staticmethod
    def player0Gold1():
        """Player 0's present gold
        """
        return library.getPlayer0Gold1()

    @staticmethod
    def player0Gold2():
        """Player 0's future gold
        """
        return library.getPlayer0Gold2()

    @staticmethod
    def player1Gold0():
        """Player 1's past gold
        """
        return library.getPlayer1Gold0()

    @staticmethod
    def player1Gold1():
        """Player 1's present gold
        """
        return library.getPlayer1Gold1()

    @staticmethod
    def player1Gold2():
        """Player 1's future gold
        """
        return library.getPlayer1Gold2()

    @staticmethod
    def playerID():
        """Player Number; either 0 or 2
        """
        return library.getPlayerID()

    @staticmethod
    def turnNumber():
        return library.getTurnNumber()

    @staticmethod
    def getTypeFromUnit(unit):
        from GameObject import UnitType
        """Returns type of supplied unit
        """
        return UnitType(library.getTypeFromUnit(unit.ptr))

    @staticmethod
    def getTypeFromBuilding(building):
        from GameObject import BuildingType
        """Returns type of supplied building
        """
        return BuildingType(library.getTypeFromBuilding(building.ptr))

    @staticmethod
    def canMove(x, y, z):
        """Returns true if movement to the square is possible
        """
        return library.canMove(x, y, z)

    @staticmethod
    def canBuild(x, y, z):
        """Returns true if building on the square is possible
        """
        return library.canBuild(x, y, z)

    @staticmethod
    def effDamage(unitType, level):
        """Attack damage of unitType at level
        """
        return library.effDamage(unitType.ptr, level)

    @staticmethod
    def effFood(buildingType, level):
        """Food produced by building at specified level
        """
        return library.effFood(buildingType.ptr, level)

    @staticmethod
    def getGold(playerNum, z):
        """Player's gold in specified time period
        """
        return library.getGold(playerNum, z)

    @staticmethod
    def artWorth(artistLevel, galleryLevel):
        """Amount of gold generated by artist at specified level
        at gallery of specified level
        """
        return library.artWorth(artistLevel, galleryLevel)

    @staticmethod
    def hunger(playerID, z):
       """Hunger damage to specified player in time period z
       """
       return library.hunger(playerID, z)

    @staticmethod
    def foodProduced(playerID, z):
        """Amount of food player produces in time period z
        """
        return library.foodProduced(playerID, z)

    @staticmethod
    def effBuildingPrice(buildingType, level):
        """Effective price of building at specified level
        """
        library.effBuildingPrice(buildingType.ptr, level)

    @staticmethod
    def effUnitPrice(unitType, level):
        """Effective price of unit at specified level
        """
        library.effUnitPrice(unitType.ptr, level)

    @staticmethod
    def effMaxHP(unitType, level):
        """Effective max HP of unit at specified level
        """
        return library.effMaxHP(unitType.ptr, level)

    @staticmethod
    def effBuildingArmor(buildingType, level):
        """Armor value of building at specified level
        """
        return library.effBuildingArmor(buildingType.ptr, level)

    @staticmethod
    def effUnitArmor(unitType, level):
       """Armor value of unit at specified level
       """
       return library.effUnitArmor(unitType.ptr, level)

