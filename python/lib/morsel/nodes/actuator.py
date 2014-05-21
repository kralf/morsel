from morsel.math import *
from object import Object

#-------------------------------------------------------------------------------

class Actuator(Object):
  def __init__(self, actuated = None, limits = [], **kargs):
    self._actuated = None
    
    super(Actuator, self).__init__(**kargs)
      
    self.actuated = actuated
    self.limits = limits
    self.command = [0]*len(limits)
    self.state = [0]*len(limits)    

    if self.world:
      self.world.addActuator(self)
    
#-------------------------------------------------------------------------------

  def getActuated(self):
    return self._actuated
    
  def setActuated(self, actuated):
    if self._actuated:
      self._actuated._actuator = None
      
    self._actuated = actuated
    
    if self._actuated:
      self._actuated._actuator = self

  actuated = property(getActuated, setActuated)
      
#-------------------------------------------------------------------------------

  def getCommand(self):
    return self._command

  def setCommand(self, command):
    self._command = [0]*len(self.limits)
    
    for i in range(min(len(self.limits), len(command))):
      self._command[i] = max(self.limits[i][0],
        min(self.limits[i][1], command[i]))

  command = property(getCommand, setCommand)

#-------------------------------------------------------------------------------

  def getAccelerationFromVelocities(self, currentVelocity, targetVelocity,
      maxAcceleration, maxDeceleration):
    if targetVelocity*currentVelocity >= 0:
      if abs(targetVelocity) > abs(currentVelocity):
        acceleration = maxAcceleration
      else:
        acceleration = maxDeceleration
    else:
      acceleration = maxAcceleration
    
    return signum(targetVelocity-currentVelocity)*acceleration

#-------------------------------------------------------------------------------

  def getAccelerationFromPositions(self, currentPosition, targetPosition,
      currentVelocity, maxVelocity, maxAcceleration, maxDeceleration):
    d_s = targetPosition-currentPosition
    s_d = signum(currentVelocity)*0.5*currentVelocity**2/maxDeceleration
    
    if d_s*s_d >= 0:
      if abs(d_s) > abs(s_d):
        return self.getAccelerationFromVelocities(currentVelocity,
          signum(d_s)*maxVelocity, maxAcceleration, maxDeceleration)
      else:
        return -signum(currentVelocity)*maxDeceleration
    else:
      return -signum(currentVelocity)*maxDeceleration
    
#-------------------------------------------------------------------------------

  def updateState(self, period):
    pass
  
#-------------------------------------------------------------------------------

  def move(self, period):
    pass
  
#-------------------------------------------------------------------------------

  def step(self, period):
    self.updateState(period)
    self.move(period)
  