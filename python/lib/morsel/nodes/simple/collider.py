from morsel.panda import *
from morsel.nodes.collider import Collider as Base

#-------------------------------------------------------------------------------

class Collider(Base):
  def __init__(self, world, name, parent = None, **kargs):
    node = panda.CollisionNode(parent.name+"Collisions")
    self.path = parent.attachNewNode(node)

    Base.__init__(self, world, name, parent = parent, **kargs)
    
    world.addCollider(self)

#-------------------------------------------------------------------------------

  def setCollisionMasks(self, collisionMasks):
    Base.setCollisionMasks(self, collisionMasks)
    
    self.path.node().setFromCollideMask(collisionMasks[0])
    self.path.node().setIntoCollideMask(collisionMasks[1])

  collisionMasks = property(Base.getCollisionMasks, setCollisionMasks)

#-------------------------------------------------------------------------------

  def addSolid(self, solid):
    Base.addSolid(self, solid)
    if solid.geometry:
      self.path.node().addSolid(solid.geometry)

#-------------------------------------------------------------------------------

  def show(self):
    Base.show(self)
    self.path.show()

#-------------------------------------------------------------------------------

  def hide(self):
    self.path.hide()
    Base.hide(self)
