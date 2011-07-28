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
      if solid.geometry:
        solid.setCollisionMasks(collisionMasks[0], collisionMasks[1])

  collisionMasks = property(Base.getCollisionMasks, setCollisionMasks)

#-------------------------------------------------------------------------------

  def addSolid(self, solid):
    Base.addSolid(self, solid)
    if solid.geometry:
      solid.geometry.setCollisionMasks(self.collisionMasks)
