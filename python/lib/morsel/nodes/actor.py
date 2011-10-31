from morsel.world.globals import *
from node import Node
from facade import Collider, Solid

#-------------------------------------------------------------------------------

class Actor(Node):
  def __init__(self, world, name, actuator = None, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.actuator = actuator
    if self.actuator:
      self.parent = self.actuator
      self.collider = self.actuator.collider
      self.collider.collisionMasks = [ACTOR_COLLISIONS_FROM,
        ACTOR_COLLISIONS_INTO]
      self.solid = self.actuator.solid
    else:
      self.collider = Collider(name+"Collider", parent = self,
        collisionMasks = [ACTOR_COLLISIONS_FROM, ACTOR_COLLISIONS_INTO])
      self.solid = Solid(name+"Solid", "Empty", self, parent = self)
