from globals import *
from object import Object
from morsel.nodes.facade import Collider

#-------------------------------------------------------------------------------

class Sensor(Object):
  def __init__(self, world, name, collisionMasks = [SENSOR_COLLISIONS_FROM,
      SENSOR_COLLISIONS_INTO], **kargs):
    Object.__init__(self, world, name, **kargs)

    self.collider = Collider(name = name+"Collider", parent = self,
      collisionMasks = collisionMasks)

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    pass

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    pass
