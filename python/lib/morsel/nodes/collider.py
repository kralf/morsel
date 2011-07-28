from morsel.world.globals import *
from collection import Collection
from iterator import Iterator
from solid import Solid

#-------------------------------------------------------------------------------

class Collider(Collection):
  def __init__(self, world, name, collisionMasks = [NO_COLLISIONS_FROM,
      NO_COLLISIONS_INTO], **kargs):
    Collection.__init__(self, world, name, **kargs)
    
    self.hide()

    self.collisionMasks = collisionMasks

#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

#-------------------------------------------------------------------------------

  def getCollisionMasks(self):
    return self._collisionMasks

  def setCollisionMasks(self, collisionMasks):
    self._collisionMasks = collisionMasks

  collisionMasks = property(getCollisionMasks, setCollisionMasks)

#-------------------------------------------------------------------------------

  def addSolid(self, solid):
    solid.parent = self
