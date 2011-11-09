from morsel.world.globals import *
from node import Node
from facade import Collider, Solid

#-------------------------------------------------------------------------------

class Actuated(Node):
  def __init__(self, world, name, actuator = None,
      collisionMasks = [NO_COLLISIONS_FROM, NO_COLLISIONS_INTO], **kargs):
    Node.__init__(self, world, name, **kargs)

    self.actuator = actuator
    if self.actuator:
      self.parent = self.actuator
      self.collider = self.actuator.collider
      self.collider.collisionMasks = collisionMasks
      self.solid = self.actuator.solid
    else:
      self.collider = Collider(name+"Collider", parent = self,
        collisionMasks = collisionMasks)
      self.solid = Solid(name+"Solid", "Empty", self, parent = self)
      
#-------------------------------------------------------------------------------

  def getLabel(self, name):
    if self.actuator:
      return self.actuator.getLabel(name)
    else:
      return Node.getLabel(self, name)

  def setLabel(self, name, label):
    if self.actuator:
      self.actuator.setLabel(name, label)
    else:
      Node.setLabel(self, name, label)
