from morsel.world.globals import *
from node import Node
from morsel.nodes.facade import Collider

#-------------------------------------------------------------------------------

class Sensor(Node):
  def __init__(self, world, name, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.collider = Collider(name = name+"Collider", parent = self,
      collisionMasks = [SENSOR_COLLISIONS_FROM, SENSOR_COLLISIONS_INTO])

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    pass

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    pass
