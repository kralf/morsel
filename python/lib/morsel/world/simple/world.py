from morsel.core import *
from morsel.world import World as Base

import morsel.nodes
import morsel.nodes.simple

#-------------------------------------------------------------------------------

class World(Base):
  def __init__(self, period = 0.01, showCollisions = False):
    Base.__init__(self, "simple")

    self.period = period
    self.showCollisions = showCollisions

    self.delta = 0
    self.lastTime = 0

    base.cTrav = panda.CollisionTraverser()
    self.pushHandler = panda.CollisionHandlerPusher()

    scheduler.addTask("WorldUpdater", self.update)
    
#-------------------------------------------------------------------------------

  def getShowCollisions(self):
    return self._showCollisions

  def setShowCollisions(self, showCollisions):
    self._showCollisions = showCollisions
    
    if self._showCollisions:
      base.cTrav.showCollisions(self.scene)

  showCollision = property(getShowCollisions, setShowCollisions)

#-------------------------------------------------------------------------------

  def addCollider(self, collider):
    base.cTrav.addCollider(collider.path, self.pushHandler)
    self.pushHandler.addCollider(collider.path, collider.parent)

#-------------------------------------------------------------------------------
  
  def update(self, time):
    self.delta += time-self.lastTime
    update = self.delta > self.period
    
    while self.delta > self.period:
      for actor in self.scene.actors:
        actor.updatePhysics(self.period)
      for platform in self.scene.platforms:
        platform.updatePhysics(self.period)
      self.delta -= self.period

    if update:
      for actor in self.scene.actors:
        actor.updateGraphics()
      for platform in self.scene.platforms:
        platform.updateGraphics()
        
    self.lastTime = time
    return True
    