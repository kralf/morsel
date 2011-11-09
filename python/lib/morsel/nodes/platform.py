from morsel.world.globals import *
from actuated import Actuated

#-------------------------------------------------------------------------------

class Platform(Actuated):
  def __init__(self, world, name,
      collisionMasks = [PLATFORM_COLLISIONS_FROM, PLATFORM_COLLISIONS_INTO],
      **kargs):
    Actuated.__init__(self, world, name, collisionMasks = collisionMasks,
      **kargs)

#-------------------------------------------------------------------------------

  def getPose(self, node = None):
    pose = self.getPosition(node)
    pose.extend(self.getOrientation(node))

    return pose

  def setPose(self, pose, node = None):
    self.setPosition(pose[0:3], node)
    self.setOrientation(pose[3:3], node)
    
  pose = property(getPose, setPose)
