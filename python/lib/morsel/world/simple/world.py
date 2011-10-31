from morsel.panda import *
from morsel.world import World as Base

#-------------------------------------------------------------------------------

class World(Base):
  def __init__(self, period = 0.01, showCollisions = False):
    Base.__init__(self, "simple", period)

    self.showCollisions = showCollisions
    base.cTrav = panda.CollisionTraverser()
    self.pushHandler = panda.CollisionHandlerPusher()
    
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
  
  def updatePhysics(self, period):
    for actuator in self.actuators:
      actuator.updatePhysics(self.period)
    for sensor in self.sensors:
      sensor.updatePhysics(self.period)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    for actuator in self.actuators:
      actuator.updateGraphics()
    for sensor in self.sensors:
      sensor.updateGraphics()
    for view in self.views:
      view.update()
    