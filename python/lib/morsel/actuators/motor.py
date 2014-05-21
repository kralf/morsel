from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes import Actuator

#-------------------------------------------------------------------------------

class Motor(Actuator):
  def __init__(self, mesh = None, maxVelocity = [], maxAcceleration = [],
      maxDeceleration = [], **kargs):
    limits = []
    for limit in maxVelocity:
      limits.append((-abs(limit), abs(limit)))
      
    super(Motor, self).__init__(limits = limits, **kargs)

    if mesh:
      self.mesh = Mesh(filename = mesh, flatten = True)

    self.maxVelocity = maxVelocity
    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration
      
#-------------------------------------------------------------------------------

  def setActuated(self, actuated):
    if self.actuated:
      self.actuated.detachNode()
      
    Actuator.setActuated(self, actuated)
    
    if self.actuated:
      self.actuated.parent = self
      self.actuated.clearTransform()

  actuated = property(Actuator.getActuated, setActuated)
  
#-------------------------------------------------------------------------------

  def getVelocity(self):
    return self.state

  def setVelocity(self, velocity):
    self.command = velocity

  velocity = property(getVelocity, setVelocity)

#-------------------------------------------------------------------------------

  def getMaxVelocity(self):
    maxVelocity = [0]*len(self.limits)
    
    for i in range(len(self.limits)):
      maxVelocity[i] = self.limits[i][1]
    
    return maxVelocity

  def setMaxVelocity(self, maxVelocity):
    if not isinstance(maxVelocity, list):
      maxVelocity = [maxVelocity]*len(self.limits)
    
    for i in range(len(self.limits)):
      self.limits[i] = (-maxVelocity[i], maxVelocity[i])

  maxVelocity = property(getMaxVelocity, setMaxVelocity)

#-------------------------------------------------------------------------------

  def getMaxAcceleration(self):
    return self._maxAcceleration

  def setMaxAcceleration(self, maxAcceleration):
    if not isinstance(maxAcceleration, list):
      self._maxAcceleration = [maxAcceleration]*len(self.limits)
    else:
      self._maxAcceleration = maxAcceleration

  maxAcceleration = property(getMaxAcceleration, setMaxAcceleration)

#-------------------------------------------------------------------------------

  def getMaxDeceleration(self):
    return self._maxDeceleration

  def setMaxDeceleration(self, maxDeceleration):
    if not isinstance(maxDeceleration, list):
      self._maxDeceleration = [maxDeceleration]*len(self.limits)
    else:
      self._maxDeceleration = maxDeceleration

  maxDeceleration = property(getMaxDeceleration, setMaxDeceleration)

#-------------------------------------------------------------------------------

  def updateState(self, period):
    for i in range(len(self.command)):
      d_v = self.command[i]-self.state[i]
      a_v = self.getAccelerationFromVelocities(self.state[i],
        self.command[i], self.maxAcceleration[i], self.maxDeceleration[i])
      if abs(a_v*period) > abs(d_v):
        self.state[i] = self.command[i]
      else:
        self.state[i] += a_v*period
      if abs(self.state[i]) > self.maxVelocity[i]:
        self.state[i] = signum(self.state[i])*self.maxVelocity[i]
  