from morsel.panda import *
from morsel.nodes.panda.object import Object
from morsel.world import World as Base

#-------------------------------------------------------------------------------

class World(Base):
  def __init__(self, period = 0.01, collisionHandler = None, showCollisions =
      False, **kargs):
    super(World, self).__init__(physics = "panda", period = period, **kargs)
    
    base.cTrav = panda.CollisionTraverser()

    self.collisionHandler = collisionHandler
    self.showCollisions = showCollisions
    
#-------------------------------------------------------------------------------

  def getShowCollisions(self):
    return self._showCollisions

  def setShowCollisions(self, showCollisions):
    self._showCollisions = showCollisions
    
    if self._showCollisions:
      base.cTrav.showCollisions(self.scene)
    else:
      base.cTrav.hideCollisions()

  showCollision = property(getShowCollisions, setShowCollisions)

#-------------------------------------------------------------------------------

  def addCollider(self, collider, object):
    if self.collisionHandler:
      base.cTrav.addCollider(collider, self.collisionHandler)
      self.collisionHandler.addCollider(collider, object)
  