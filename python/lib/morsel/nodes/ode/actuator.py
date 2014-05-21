from morsel.nodes.actuator import Actuator as Base
from object import Object

#-------------------------------------------------------------------------------

class Actuator(Object, Base):
  COLLISIONS_FROM = 0x000000F0
  COLLISIONS_INTO = 0xFFF00F0F
  
  def __init__(self, collisionMasks = [COLLISIONS_FROM, COLLISIONS_INTO],
      **kargs):
    super(Actuator, self).__init__(collisionMasks = collisionMasks, **kargs)
    
#-------------------------------------------------------------------------------

  def getForceFromVelocities(self, currentVelocity, targetVelocity,
      maxAccelerationForce, maxDecelerationForce):
    if targetVelocity*currentVelocity >= 0:
      if abs(targetVelocity) > abs(currentVelocity):
        force = maxAccelerationForce
      else:
        force = maxDecelerationForce
    else:
      force = maxAccelerationForce
    
    return signum(targetVelocity-currentVelocity)*force
    