from globals import *
from object import Object
from facade import Collider, Solid

#-------------------------------------------------------------------------------

class Actuated(Object):
  def __init__(self, world, name, actuator = None, collisionMasks =
      [NO_COLLISIONS_FROM, NO_COLLISIONS_INTO], **kargs):
    Object.__init__(self, world, name, **kargs)

    self.actuator = actuator
    if self.actuator:
      self.parent = self.actuator
      self.collider = self.actuator.collider
      self.collider.collisionMasks = collisionMasks
      self.solid = Solid(name = name+"Solid", type = "Empty", mesh = self,
        parent = self.actuator.solid)
    else:
      self.collider = Collider(name = name+"Collider", parent = self,
        collisionMasks = collisionMasks)
      self.solid = Solid(name = name+"Solid", type = "Empty", mesh = self,
        parent = self)
      
#-------------------------------------------------------------------------------

  def getLabel(self, name):
    if self.actuator:
      return self.actuator.getLabel(name)
    else:
      return Object.getLabel(self, name)

  def setLabel(self, name, label):
    if self.actuator:
      self.actuator.setLabel(name, label)
    else:
      Object.setLabel(self, name, label)
