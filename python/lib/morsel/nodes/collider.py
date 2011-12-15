from globals import *
from object import Object
from iterator import Iterator
from solid import Solid

#-------------------------------------------------------------------------------

class Collider(Object):
  def __init__(self, name, world, collisionMasks = [NO_COLLISIONS_FROM,
      NO_COLLISIONS_INTO], **kargs):
    Object.__init__(self, name, world, **kargs)
    
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
    solid.collider = self
