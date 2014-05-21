from morsel.panda import *
from morsel.math import *
from morsel.actuators.drive import Drive

#-------------------------------------------------------------------------------

class PlanarDrive(Drive):
  def __init__(self, bearingMesh = None, bearingHidden = True, maxVelocity = 
      [0, 0, 0], maxAcceleration = [0, 0, 0], maxDeceleration = [0, 0, 0],
      **kargs):
    limits = [(-maxVelocity[0], maxVelocity[0]),
              (-maxVelocity[1], maxVelocity[1]),
              (-maxVelocity[2], maxVelocity[2])]
      
    super(PlanarDrive, self).__init__(mesh = bearingMesh, limits = limits,
      **kargs)
    
    if bearingHidden:
      self.mesh.hide()

    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration
    
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
    return [self.limits[0][1], self.limits[1][1]]

  def setMaxLinearVelocity(self, maxLinearVelocity):
    if not isinstance(maxLinearVelocity, list):
      maxLinearVelocity = [maxLinearVelocity]*2
      
    self.limits = [(-maxLinearVelocity[0], maxLinearVelocity[0]),
                   (-maxLinearVelocity[1], maxLinearVelocity[1]),
                   self.limits[2]]

  maxLinearVelocity = property(getMaxLinearVelocity, setMaxLinearVelocity)

#-------------------------------------------------------------------------------

  def getMaxAngularVelocity(self):
    return self.limits[2][1]

  def setMaxAngularVelocity(self, maxAngularVelocity):
    self.limits = [self.limits[0], self.limits[1],
                   (-maxAngularVelocity, maxAngularVelocity)]

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

  def updateState(self, period):
    for i in range(len(self.command)):
      d_v = self.command[i]-self.state[i]
      a_v = self.getAccelerationFromVelocities(self.state[i],
        self.command[i], self.maxAcceleration[i], self.maxDeceleration[i])
      if abs(a_v*period) > abs(d_v):
        self.state[i] = self.command[i]
      else:
        self.state[i] += a_v*period
      if abs(self.state[i]) > self.limits[i][1]:
        self.state[i] = signum(self.state[i])*self.limits[i][1]
        
#-------------------------------------------------------------------------------

  def move(self, period):
    if self.actuated:
      d_x = self.linearVelocity[0]*period
      d_y = self.linearVelocity[1]*period
      d_quat = Quaternion()
      d_quat.orientation = [self.angularVelocity*period, 0, 0]

      self.actuated.position = (panda.Vec3(*self.actuated.position)+
        self.actuated.parent.getRelativeVector(self.actuated,
        panda.Vec3(d_x, d_y, 0)))
      self.actuated.quaternion *= d_quat
