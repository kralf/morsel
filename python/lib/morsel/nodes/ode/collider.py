from morsel.core import *
from morsel.nodes.collider import Collider as Base

#-------------------------------------------------------------------------------

class Collider(Base):
  def __init__(self, world, name, **kargs):
    Base.__init__(self, world, name, **kargs)
    
#-------------------------------------------------------------------------------

  def setCollisionMasks(self, collisionMasks):
    Base.setCollisionMasks(self, collisionMasks)

    for solid in self.solids:
      solid.setCollisionMasks(collisionMasks)

  collisionMasks = property(Base.getCollisionMasks, setCollisionMasks)

#-------------------------------------------------------------------------------

  def addSolid(self, solid):
    Base.addSolid(self, solid)
    solid.collisionMasks = self.collisionMasks
