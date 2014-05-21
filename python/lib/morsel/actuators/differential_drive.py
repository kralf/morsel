from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Object, Mesh
from morsel.actuators.wheel_drive import WheelDrive

#-------------------------------------------------------------------------------

class DifferentialDrive(WheelDrive):
  def __init__(self, casterCrankMeshes = [], maxVelocity = [0, 0],
      maxAcceleration = [0, 0], maxDeceleration = [0, 0], **kargs):
    limits = [(-maxVelocity[0], maxVelocity[0]),
              (-maxVelocity[1], maxVelocity[1])]
      
    super(DifferentialDrive, self).__init__(limits = limits, **kargs)
      
    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration
    
    self.casterCranks = []
    self.casterWheels = []
    self.casterRadii = []
    self.casterDistances = []
    self.casterAzimuths = []
    
    self.casterRates = []

    numCasters = min(len(self.wheels), len(casterCrankMeshes))    
    for i in range(numCasters) :
      casterWheel = self.wheels[-numCasters+i]
      casterCrankMesh = Mesh(filename = casterCrankMeshes[i], exclude =
        casterWheel.mesh.modelName, flatten = True)
      casterCrank = Object(name = "Caster%d" % i, mesh = casterCrankMesh,
        parent = self)
      casterWheel.parent = casterCrank

      self.casterCranks.append(casterCrank)
      self.casterWheels.append(casterWheel)
      
      casterPosition = panda.Vec3(*casterCrank.getPosition(self))
      casterPosition[2] = 0
      self.casterDistances.append(casterPosition.length())
      casterPosition.normalize()
      self.casterAzimuths.append(panda.Vec3(1, 0, 0).signedAngleDeg(
        casterPosition, panda.Vec3(0, 0, 1)))
        
      wheelPosition = casterWheel.getPos(casterCrank)
      wheelPosition[2] = 0
      self.casterRadii.append(wheelPosition.length())
      
      self.casterRates.append(0)

#-------------------------------------------------------------------------------

  def getLinearVelocity(self):
    return self.state[0]

  def setLinearVelocity(self, linearVelocity):
    if isinstance(linearVelocity, list):
      linearVelocity = linearVelocity[0]
      
    self.command = [linearVelocity, self.command[1]]

  linearVelocity = property(getLinearVelocity, setLinearVelocity)

#-------------------------------------------------------------------------------

  def getAngularVelocity(self):
    return self.state[1]

  def setAngularVelocity(self, angularVelocity):
    if isinstance(angularVelocity, list):
      angularVelocity = angularVelocity[0]
      
    self.command = [self.command[0], angularVelocity]

  angularVelocity = property(getAngularVelocity, setAngularVelocity)

#-------------------------------------------------------------------------------

  def getMaxLinearVelocity(self):
    return self.limits[0][1]
    
  def setMaxLinearVelocity(self, maxLinearVelocity):
    self.limits = [(-maxLinearVelocity, maxLinearVelocity), self.limits[1]]

  maxLinearVelocity = property(getMaxLinearVelocity, setMaxLinearVelocity)
                   
#-------------------------------------------------------------------------------

  def getMaxAngularVelocity(self):
    return self.limits[1][1]
    
  def setMaxAngularVelocity(self, maxAngularVelocity):
    self.limits = [self.limits[0], (-maxAngularVelocity, maxAngularVelocity)]

  maxAngularVelocity = property(getMaxAngularVelocity, setMaxAngularVelocity)
                   
#-------------------------------------------------------------------------------

  def getMaxLinearAcceleration(self):
    return self.maxAcceleration[0]
    
  def setMaxLinearAcceleration(self, maxLinearAcceleration):
    self.maxAcceleration[0] = maxLinearAcceleration

  maxLinearAcceleration = property(getMaxLinearAcceleration,
    setMaxLinearAcceleration)
                   
#-------------------------------------------------------------------------------

  def getMaxAngularAcceleration(self):
    return self.maxAcceleration[1]
    
  def setMaxAngularAcceleration(self, maxAngularAcceleration):
    self.maxAcceleration[1] = maxAngularAcceleration

  maxAngularAcceleration = property(getMaxAngularAcceleration,
    setMaxAngularAcceleration)
                   
#-------------------------------------------------------------------------------

  def getMaxLinearDeceleration(self):
    return self.maxDeceleration[0]
    
  def setMaxLinearDeceleration(self, maxLinearDeceleration):
    self.maxDeceleration[0] = maxLinearDeceleration

  maxLinearDeceleration = property(getMaxLinearDeceleration,
    setMaxLinearDeceleration)
  
#-------------------------------------------------------------------------------

  def getMaxAngularDeceleration(self):
    return self.maxDeceleration[1]
    
  def setMaxAngularDeceleration(self, maxAngularDeceleration):
    self.maxDeceleration[1] = maxAngularDeceleration

  maxAngularDeceleration = property(getMaxAngularDeceleration,
    setMaxAngularDeceleration)
  
#-------------------------------------------------------------------------------

  def getCasterAngles(self):
    casterAngles = [0]*len(self.casterCranks)
    
    for i in range(len(self.casterCranks)):
      casterAngles[i] = self.casterCranks[i].yaw
    
    return casterAngles
  
  def setCasterAngles(self, casterAngles):
    if not isinstance(casterAngles, list):
      casterAngles = [casterAngles]*len(self.casterCranks)
      
    for i in range(len(self.casterCranks)):
      self.casterCranks[i].yaw = casterAngles[i]

  casterAngles = property(getCasterAngles, setCasterAngles)

#-------------------------------------------------------------------------------

  def getWheelRatesFromState(self, linearVelocity, angularVelocity):
    wheelRates = [0]*len(self.wheels)
    casterAngles = self.casterAngles

    for i in range(len(self.wheels)):
      if self.isCasterWheel(self.wheels[i]):
        j = self.casterWheels.index(self.wheels[i])
        psi = self.casterCranks[j].yaw*pi/180
        theta = self.casterAzimuths[j]*pi/180

        wheelRates[i] = ((linearVelocity*cos(psi)+cos(theta)*angularVelocity*
          pi/180*self.casterDistances[j]*sin(psi))/self.wheelRadii[i]*180/pi)
      else:
        wheelRates[i] = (((linearVelocity-self.getWheelTrack(i)*
          angularVelocity*pi/180)/self.wheelRadii[i])*180/pi)

    return wheelRates

#-------------------------------------------------------------------------------

  def getCasterRatesFromState(self, linearVelocity, angularVelocity):
    casterRates = [0]*len(self.casterCranks)

    for i in range(len(self.casterCranks)):
      psi = self.casterCranks[i].yaw*pi/180
      theta = self.casterAzimuths[i]*pi/180
      
      casterRates[i] = ((1/self.casterRadii[i]*(cos(theta)*angularVelocity*
        pi/180*(self.casterDistances[i]*cos(psi)+self.casterRadii[i])-
        linearVelocity*sin(psi)))*180/pi)

    return casterRates

#-------------------------------------------------------------------------------

  def isCasterWheel(self, wheel):
    return wheel in self.casterWheels

#-------------------------------------------------------------------------------

  def updateState(self, period):
    d_v = self.command[0]-self.state[0]
    a_v = self.getAccelerationFromVelocities(self.state[0],
      self.command[0], self.maxAcceleration[0], self.maxDeceleration[0])
    if abs(a_v*period) > abs(d_v):
      self.state[0] = self.command[0]
    else:
      self.state[0] += a_v*period
    if abs(self.state[0]) > self.maxLinearVelocity:
      self.state[0] = signum(self.state[0])*self.maxLinearVelocity

    d_w = self.command[1]-self.state[1]
    a_w = self.getAccelerationFromVelocities(self.state[1],
      self.command[1], self.maxAcceleration[1], self.maxDeceleration[1])
    if abs(a_w*period) > abs(d_w):
      self.state[1] = self.command[1]
    else:
      self.state[1] += a_w*period
    if abs(self.state[1]) > self.maxAngularVelocity:
      self.state[1] = signum(self.state[1])*self.maxAngularVelocity
      
    self.casterRates = self.getCasterRatesFromState(
      self.state[0], self.state[1])
    self.wheelRates = self.getWheelRatesFromState(
      self.state[0], self.state[1])
    
#-------------------------------------------------------------------------------

  def move(self, period):
    d_theta = self.state[1]*pi/180*period
    d_x = self.state[0]*cos(d_theta)*period
    d_y = self.state[0]*sin(d_theta)*period

    if self.actuated:
      self.actuated.x += (d_x*cos(self.actuated.yaw*pi/180)-
        d_y*sin(self.actuated.yaw*pi/180))
      self.actuated.y += (d_x*sin(self.actuated.yaw*pi/180)+
        d_y*cos(self.actuated.yaw*pi/180))
      self.actuated.yaw += d_theta*180/pi    

    for i in range(len(self.casterCranks)):
      self.casterCranks[i].yaw += self.casterRates[i]*period
        
    WheelDrive.move(self, period)
    