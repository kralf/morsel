from morsel.panda import *
from morsel.math import *
from morsel.actuators.motor import Motor

#-------------------------------------------------------------------------------

class PlanarMotor(Motor):
  def __init__(self, axes = [[1, 0, 0], [0, 1, 0]], minPosition =
      [-float("inf"), -float("inf")], maxPosition = [float("inf"),
      float("inf")], minAngle = -float("inf"), maxAngle = float("inf"),
      maxVelocity = [0, 0, 0], maxAcceleration = [0, 0, 0],
      maxDeceleration = [0, 0, 0], **kargs):
    super(PlanarMotor, self).__init__(maxVelocity = maxVelocity,
      maxAcceleration = maxAcceleration, maxDeceleration = maxDeceleration,
      **kargs)

    self.axes = axes
    self.minPosition = minPosition
    self.maxPosition = maxPosition
    self.minAngle = minAngle
    self.maxAngle = maxAngle
    
#-------------------------------------------------------------------------------

  def getLinearVelocity(self):
    return self.state[0:2]

  def setLinearVelocity(self, linearVelocity):
    if not isinstance(linearVelocity, list):
      linearVelocity = [linearVelocity]*2
    elif len(linearVelocity) == 3:
      linearVelocity = linearVelocity[0:2]
    
    self.command[0:2] = linearVelocity

  linearVelocity = property(getLinearVelocity, setLinearVelocity)

#-------------------------------------------------------------------------------

  def getAngularVelocity(self):
    return self.state[2]

  def setAngularVelocity(self, angularVelocity):
    if isinstance(angularVelocity, list):
      angularVelocity = angularVelocity[0]
      
    self.command[2] = angularVelocity

  angularVelocity = property(getAngularVelocity, setAngularVelocity)

#-------------------------------------------------------------------------------

  def getMaxLinearVelocity(self):
    return self.maxVelocity[0:2]

  def setMaxLinearVelocity(self, maxLinearVelocity):
    if not isinstance(maxLinearVelocity, list):
      maxLinearVelocity = [maxLinearVelocity]*2
      
    self.maxVelocity[0:2] = maxLinearVelocity

  maxLinearVelocity = property(getMaxLinearVelocity, setMaxLinearVelocity)

#-------------------------------------------------------------------------------

  def getMaxAngularVelocity(self):
    return self.maxVelocity[2]

  def setMaxAngularVelocity(self, maxAngularVelocity):
    self.maxVelocity[2] = maxAngularVelocity

  maxAngularVelocity = property(getMaxAngularVelocity, setMaxAngularVelocity)

#-------------------------------------------------------------------------------

  def getMaxLinearAcceleration(self):
    return self.maxAcceleration[0:2]

  def setMaxLinearAcceleration(self, maxLinearAcceleration):
    if not isinstance(maxLinearAcceleration, list):
      maxLinearAcceleration = [maxLinearAcceleration]*2
      
    self.maxAcceleration[0:2] = maxLinearAcceleration

  maxLinearAcceleration = property(getMaxLinearAcceleration,
    setMaxLinearAcceleration)

#-------------------------------------------------------------------------------

  def getMaxAngularAcceleration(self):
    return self.maxAcceleration[2]

  def setMaxAngularAcceleration(self, maxAngularAcceleration):
    self.maxAcceleration[2] = maxAngularAcceleration

  maxAngularAcceleration = property(getMaxAngularAcceleration,
    setMaxAngularAcceleration)

#-------------------------------------------------------------------------------

  def getMaxLinearDeceleration(self):
    return self.maxDeceleration[0:2]

  def setMaxLinearDeceleration(self, maxLinearDeceleration):
    if not isinstance(maxLinearDeceleration, list):
      maxLinearDeceleration = [maxLinearDeceleration]*2
      
    self.maxDeceleration[0:2] = maxLinearDeceleration

  maxLinearDeceleration = property(getMaxLinearDeceleration,
    setMaxLinearDeceleration)

#-------------------------------------------------------------------------------

  def getMaxAngularDeceleration(self):
    return self.maxDeceleration[2]

  def setMaxAngularDeceleration(self, maxAngularDeceleration):
    self.maxDeceleration[2] = maxAngularDeceleration

  maxAngularDeceleration = property(getMaxAngularDeceleration,
    setMaxAngularDeceleration)

#-------------------------------------------------------------------------------

  def getAxisPosition(self):
    axisPosition = [float("nan")]*2
      
    if self.actuated:
      position = panda.Vec3(*self.actuated.position)
        
      for i in [0, 1]:      
        axis = panda.Vec3(*self.axes[i])
        axis.normalize()
      
        axisPosition[i] = position.dot(axis)
        
    return axisPosition
  
  def setAxisPosition(self, axisPosition):
    if self.actuated:
      if not isinstance(axisPosition, list):
        axisPosition = [axisPosition]*2
      
      position = panda.Vec3(0, 0, 0)
      
      for i in [0, 1]:      
        axis = panda.Vec3(*self.axes[i])
        axis.normalize()
      
        if axisPosition[i] < self.minPosition[i]:
          axisPosition[i] = self.minPosition[i]
        elif axisPosition[i] > self.maxPosition[i]:
          axisPosition[i] = self.maxPosition[i]
          
        position += axis*axisPosition[i]
        
      self.actuated.position = [position[0], position[1], position[2]]
      
  axisPosition = property(getAxisPosition, setAxisPosition)

#-------------------------------------------------------------------------------

  def getAxisAngle(self):
    if self.actuated:
      axis = panda.Vec3(*self.axes[0]).cross(panda.Vec3(*self.axes[1]))
      
      if self.actuated.quaternion.getAxisNormalized().dot(axis) > 0:
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
      
      axis = panda.Vec3(*self.axes[0]).cross(panda.Vec3(*self.axes[1]))
      axis.normalize()
      
      quaternion = Quaternion()
      quaternion.setFromAxisAngle(positiveAngle(angle), axis)
      
      self.actuated.quaternion = quaternion
  
  axisAngle = property(getAxisAngle, setAxisAngle)

#-------------------------------------------------------------------------------

  def move(self, period):
    Motor.move(self, period)
    
    if self.actuated:
      position = self.axisPosition
      for i in [0, 1]:
        position[i] += self.linearVelocity[i]*period
      
      self.axisPosition = position
      self.axisAngle += self.angularVelocity*period
