import structures

client = 0
server = 1

UnitType = structures.Model('UnitType', key='objectID',
  data = ( ('objectID', int),
    ('name', str),
    ('price', int),
    ('hunger', int),
    ('traintime', int),
    ('hp', int),
    ('armor', int),
    ('moves', int),
    ('actions', int),
    ('attackcost', int),
    ('damage', int),
    ('minrange', int),
    ('maxrange', int),
    ('trainerID', int),
    ('canpaint', int))
  )

Unit = structures.Model('Unit', key='objectID',
  data = ( ('objectID', int),
    ('x', int),
    ('y', int),
    ('z', int),
    ('hp', int),
    ('level', int),
    ('unitTypeID', int),
    ('ownerIndex', int),
    ('actions', int),
    ('moves', int))
  )

BuildingType = structures.Model('BuildingType', key='objectID',
  data = ( ('objectID', int),
    ('name', str),
    ('price', int),
    ('food', int),
    ('buildtime', int),
    ('hp', int),
    ('armor', int),
    ('builderID', int),
    ('allowPaint', int),
    ('width', int),
    ('height', int),
    ('spawnX', int),
    ('spawnY', int))
  )

Building = structures.Model('Building', key='objectID',
  data = ( ('objectID', int),
    ('x', int),
    ('y', int),
    ('z', int),
    ('hp', int),
    ('level', int),
    ('buildingTypeID', int),
    ('inTraining', int),
    ('progress', int),
    ('linked', int),
    ('complete', int))
  )

"""
UnitType(Model):
  _name = 'UnitType'
  _key = 'id'
  id = int
  
  cost = (int, int) #base, incr
  hp = (int, int) #base, incr
  moves = int
  actions = int
  range = (int, int) #min, max
  damage = (int, int) #base, incr
  
  buildSpeed = int
  paintSpeed = int
  

class BuildingType(Model):
  _name = 'BuildingType'
  _key = 'id'
  id = int
  
  cost = (int, int) #base, incr
  hp = (int, int) #base, incr
  buildTime = (int, int, int) #base, incr
  builds = [UnitType]

class MappableObject(Model):
  _name = 'MappableObject'
  _key = 'id'
  id = int
  x = int
  y = int

class Unit(MappableObject):
  _name = 'Unit'
  type = UnitType
  level = int
  hp = int
  moves = int
  actions = int

class Buildng(MappableObject):
  _name = 'Building'
  type = BuildingType
  level = int
  hp = int

class PlayerStatus(Model):
  _name = 'PlayerStatus'
  name = str
  s

class Status(Message):
  _head = 'Status'
  _source = server
  _format = [int, int, [Unit]]
"""