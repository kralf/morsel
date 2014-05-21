from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh, Object
from morsel.actuators.motor import Motor

#-------------------------------------------------------------------------------

class AngularMotor(Motor):
  def __init__(self, axis = [1, 0, 0], minAngle = -float("inf"), maxAngle =
      float("inf"), maxVelocity = 0, maxAcceleration = 0, maxDeceleration = 0,
      **kargs):
    super(AngularMotor, self).__init__(maxVelocity = [maxVelocity],
      maxAcceleration = [maxAcceleration], maxDeceleration = [maxDeceleration],
      **kargs)
    
    self.axis = axis
    self.minAngle = minAngle
    self.maxAngle = maxAngle
      
#-------------------------------------------------------------------------------

  def getAngularVelocity(self):
    return self.state[0]

  def setAngularVelocity(self, angularVelocity):
    self.command[0] = angularVelocity

  angularVelocity = property(getAngularVelocity, setAngularVelocity)

#-------------------------------------------------------------------------------

  def getMaxAngularVelocity(self):
    return self.maxVelocity[0]

  def setMaxAngularVelocity(self, maxAngularVelocity):
    self.maxVelocity[0] = maxAngularVelocity

  maxAngularVelocity = property(getMaxAngularVelocity, setMaxAngularVelocity)

#-------------------------------------------------------------------------------

  def getMaxAngularAcceleration(self):
    return self.maxAcceleration[0]

  def setMaxAngularAcceleration(self, maxAngularAcceleration):
    self.maxAcceleration[0] = maxAngularAcceleration

  maxAngularAcceleration = property(getMaxAngularAcceleration,
    setMaxAngularAcceleration)

#-------------------------------------------------------------------------------

  def getMaxAngularDeceleration(self):
    return self.maxDeceleration[0]

  def setMaxAngularDeceleration(self, maxAngularDeceleration):
    self.maxDeceleration[0] = maxAngularDeceleration

  maxAngularDeceleration = property(getMaxAngularDeceleration,
    setMaxAngularDeceleration)

#-------------------------------------------------------------------------------

  def getMinAngle(self):
    return self._minAngle
    
  def setMinAngle(self, angle):
    self._minAngle = correctAngle(angle)
    
  minAngle = property(getMinAngle, setMinAngle)

#-------------------------------------------------------------------------------

  def getMaxAngle(self):
    return self._maxAngle
    
  def setMaxAngle(self, angle):
    self._maxAngle = correctAngle(angle)
    
  maxAngle = property(getMaxAngle, setMaxAngle)
  
#-------------------------------------------------------------------------------

  def getAxisAngle(self):
    if self.actuated:
      if self.actuated.quaternion.getAxisNormalized().dot(
          panda.Vec3(*self.axis)) > 0:
        return correctAngle(self.actuated.quaternion.getAngle())
      else:
        return correctAngle(-self.actuated.quaternion.getAngle())
    else:
      return float("nan")
  
  def setAxisAngle(self, angle):
    if self.actuated:
      if angle < self.minAngle:
        angle = self.minAngle
      elif angle > self.maxAngle:
        angle = self.maxAngle
        
      quaternion = Quaternion()
      quaternion.setFromAxisAngle(positiveAngle(angle),
        panda.Vec3(*self.axis))
      
      self.actuated.quaternion = quaternion
  
  axisAngle = property(getAxisAngle, setAxisAngle)

#-------------------------------------------------------------------------------

  def move(self, period):
    self.axisAngle += self.angularVelocity*period
