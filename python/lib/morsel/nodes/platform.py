from morsel.world.globals import *
from node import Node
from facade import Collider, Solid

#-------------------------------------------------------------------------------

class Platform(Node):
  def __init__(self, world, name, actuator = None, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.actuator = actuator
    if self.actuator:
      self.parent = self.actuator
      self.collider = self.actuator.collider
      self.collider.collisionMasks = [PLATFORM_COLLISIONS_FROM,
        PLATFORM_COLLISIONS_INTO]
      self.solid = self.actuator.solid
    else:
      self.collider = Collider(name+"Collider", parent = self,
        collisionMasks = [PLATFORM_COLLISIONS_FROM, PLATFORM_COLLISIONS_INTO])
      self.solid = Solid(name+"Solid", "Empty", self, parent = self)

#-------------------------------------------------------------------------------

  def getPose(self, node = None):
    pose = self.getPosition(node)
    pose.extend(self.getOrientation(node))

    return pose

  def setPose(self, pose, node = None):
    self.setPosition(pose[0:3], node)
    self.setOrientation(pose[3:3], node)
    
  pose = property(getPose, setPose)
