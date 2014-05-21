from morsel.panda import *
from morsel.nodes.facade import Mesh, Object
from morsel.actuators.motor import Motor

#-------------------------------------------------------------------------------

class LinearMotor(Motor):
  def __init__(self, axis = [1, 0, 0], minPosition = -float("inf"),
      maxPosition = float("inf"), maxVelocity = 0, maxAcceleration = 0,
      maxDeceleration = 0, **kargs):
    super(LinearMotor, self).__init__(maxVelocity = [maxVelocity],
      maxAcceleration = [maxAcceleration], maxDeceleration = [maxDeceleration],
      **kargs)
    
    self.axis = axis
    self.minPosition = minPosition
    self.maxPosition = maxPosition
            
#-------------------------------------------------------------------------------

  def getLinearVelocity(self):
    return self.state[0]

  def setLinearVelocity(self, linearVelocity):
    self.command[0] = linearVelocity

  linearVelocity = property(getLinearVelocity, setLinearVelocity)

#-------------------------------------------------------------------------------

  def getMaxLinearVelocity(self):
    return self.maxVelocity[0]

  def setMaxLinearVelocity(self, maxLinearVelocity):
    self.maxVelocity[0] = maxLinearVelocity

  maxLinearVelocity = property(getMaxLinearVelocity, setMaxLinearVelocity)

#-------------------------------------------------------------------------------

  def getMaxLinearAcceleration(self):
    return self.maxAcceleration[0]

  def setMaxLinearAcceleration(self, maxLinearAcceleration):
    self.maxAcceleration[0] = maxLinearAcceleration

  maxLinearAcceleration = property(getMaxLinearAcceleration,
    setMaxLinearAcceleration)

#-------------------------------------------------------------------------------

  def getMaxLinearDeceleration(self):
    return self.maxDeceleration[0]

  def setMaxLinearDeceleration(self, maxLinearDeceleration):
    self.maxDeceleration[0] = maxLinearDeceleration

  maxLinearDeceleration = property(getMaxLinearDeceleration,
    setMaxLinearDeceleration)

#-------------------------------------------------------------------------------

  def getAxisPosition(self):
    if self.actuated:
      axis = panda.Vec3(*self.axis)
      axis.normalize()
    
      position = panda.Vec3(*self.actuated.position)
      
      return position.dot(axis)
    else:
      return float("nan")
  
  def setAxisPosition(self, position):
    if self.actuated:
      axis = panda.Vec3(*self.axis)
      axis.normalize()
    
      if position < self.minPosition:
        position = self.minPosition
      elif position > self.maxPosition:
        position = self.maxPosition
        
      self.actuated.position = axis*position
      
  axisPosition = property(getAxisPosition, setAxisPosition)

#-------------------------------------------------------------------------------

  def move(self, period):
    self.axisPosition += self.linearVelocity*period
  