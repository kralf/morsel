from morsel.core import *
from morsel.nodes.collection import Collection

#-------------------------------------------------------------------------------

class Collider(Collection):
  def __init__(self, world, name, **kargs):
    Collection.__init__(self, world, name, **kargs)
    
    node = panda.CollisionNode(self.parent.name+"Collider")
    self.path = self.parent.attachNewNode(node)
    
    self.hide()

    world.addCollider(self)

#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

#-------------------------------------------------------------------------------

  def setCollisionMasks(self, collisionsFrom, collisionsInto):
    self.path.node().setFromCollideMask(collisionsFrom)
    self.parent.setCollideMask(collisionsInto)

#-------------------------------------------------------------------------------

  def addSolid(self, solid):
    self.path.node().addSolid(solid.geometry)

#-------------------------------------------------------------------------------

  def show(self):
    Collection.show(self)
    self.path.show()

#-------------------------------------------------------------------------------

  def hide(self):
    self.path.hide()
    Collection.hide(self)
