from morsel.panda import *
from morsel.math import *
from morsel.actuators.wheel_drive import WheelDrive

#-------------------------------------------------------------------------------

class AckermannDrive(WheelDrive):
  def __init__(self, maxSteeringAngle = 0, maxVelocity = [0, 0],
      maxAcceleration = [0, 0], maxDeceleration = [0, 0], epsilon = 1e-6,
      **kargs):
    limits = [(-maxVelocity[0], maxVelocity[0]),
              (-maxSteeringAngle, maxSteeringAngle)]
      
    super(AckermannDrive, self).__init__(limits = limits, **kargs)

    self.maxSteeringRate = maxVelocity[1]
    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration
    self.epsilon = epsilon    
    
    self.steeringRate = 0
    self.wheelAngles = [0, 0]
    self.wheelSteeringRates = [0, 0]
    
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
    return self.getAngularVelocityFromState(self.state[0], self.state[1])

  def setAngularVelocity(self, angularVelocity):
    if isinstance(angularVelocity, list):
      angularVelocity = angularVelocity[0]
      
    if abs(angularVelocity) >= self.epsilon:
      radius = self.command[0]/(angularVelocity*pi/180)
      if abs(radius) >= self.epsilon:
        self.command = [self.command[0],
          atan(self.wheelBase/radius)*180/pi]
    else:
      self.command = [self.command[0], 0]

  angularVelocity = property(getAngularVelocity, setAngularVelocity)

#-------------------------------------------------------------------------------

  def getSteeringAngle(self):
    return self.state[1]

  def setSteeringAngle(self, steeringAngle):
    self.command = [self.command[0], steeringAngle]

  steeringAngle = property(getSteeringAngle, setSteeringAngle)

#-------------------------------------------------------------------------------

  def getMaxSteeringAngle(self):
    return self.limits[1][1]

  def setMaxSteeringAngle(self, maxSteeringAngle):
    self.limits = [self.limits[0], (-maxSteeringAngle, maxSteeringAngle)]
    
  maxSteeringAngle = property(getMaxSteeringAngle, setMaxSteeringAngle)
    
#-------------------------------------------------------------------------------

  def getMaxLinearVelocity(self):
    return self.limits[0][1]
    
  def setMaxLinearVelocity(self, maxLinearVelocity):
    self.limits = [(-maxLinearVelocity, maxLinearVelocity), self.limits[1]]

  maxLinearVelocity = property(getMaxLinearVelocity, setMaxLinearVelocity)
                   
#-------------------------------------------------------------------------------

  def getMaxLinearAcceleration(self):
    return self.maxAcceleration[0]
    
  def setMaxLinearAcceleration(self, maxLinearAcceleration):
    self.maxAcceleration[0] = maxLinearAcceleration

  maxLinearAcceleration = property(getMaxLinearAcceleration,
    setMaxLinearAcceleration)
                   
#-------------------------------------------------------------------------------

  def getMaxSteeringAcceleration(self):
    return self.maxAcceleration[1]
    
  def setMaxSteeringAcceleration(self, maxSteeringAcceleration):
    self.maxAcceleration[1] = maxSteeringAcceleration

  maxSteeringAcceleration = property(getMaxSteeringAcceleration,
    setMaxSteeringAcceleration)
                   
#-------------------------------------------------------------------------------

  def getMaxLinearDeceleration(self):
    return self.maxDeceleration[0]
    
  def setMaxLinearDeceleration(self, maxLinearDeceleration):
    self.maxDeceleration[0] = maxLinearDeceleration

  maxLinearDeceleration = property(getMaxLinearDeceleration,
    setMaxLinearDeceleration)
                   
#-------------------------------------------------------------------------------

  def getMaxSteeringDeceleration(self):
    return self.maxDeceleration[1]
    
  def setMaxSteeringDeceleration(self, maxSteeringDeceleration):
    self.maxDeceleration[1] = maxSteeringDeceleration

  maxSteeringDeceleration = property(getMaxSteeringDeceleration,
    setMaxSteeringDeceleration)
                   
#-------------------------------------------------------------------------------

  def getFrontTrack(self):
    return self.getWheelDistance(0, 1)

  frontTrack = property(getFrontTrack)

#-------------------------------------------------------------------------------

  def getWheelBase(self):
    return 0.5*(self.getWheelDistance(0, 2)+self.getWheelDistance(1, 3))

  wheelBase = property(getWheelBase)

#-------------------------------------------------------------------------------

  def getSteeringAngleFromWheelAngles(self, wheelAngles):
    steeringAngle = 0
    
    if ((tan(wheelAngles[0]*pi/180) == 0) or 
        tan(wheelAngles[1]*pi/180) == 0):
      return steeringAngle

    cotLeftAngle = 1/tan(wheelAngles[0]*pi/180)
    cotRightAngle = 1/tan(wheelAngles[1]*pi/180)
    
    leftSteeringAngle = atan(1/(cotLeftAngle+self.frontTrack/
      (2*self.wheelBase)))*180/pi
    rightSteeringAngle = atan(1/(cotRightAngle-self.frontTrack/
      (2*self.wheelBase)))*180/pi

    return 0.5*(leftSteeringAngle+rightSteeringAngle)

#-------------------------------------------------------------------------------

  def getWheelAnglesFromSteeringAngle(self, steeringAngle):
    wheelAngles = [0, 0]
    
    if tan(steeringAngle*pi/180) == 0:
      return wheelAngles
      
    cotLeftAngle = (1/tan(steeringAngle*pi/180)-self.frontTrack/
      (2*self.wheelBase))
    cotRightAngle = (cotLeftAngle+self.frontTrack/self.wheelBase)
    
    wheelAngles[0] = atan(1/cotLeftAngle)*180/pi
    wheelAngles[1] = atan(1/cotRightAngle)*180/pi
    
    return wheelAngles

#-------------------------------------------------------------------------------

  def getAngularVelocityFromState(self, linearVelocity, steeringAngle):
    if abs(steeringAngle) >= self.epsilon:
      radius = self.wheelBase/tan(steeringAngle*pi/180)
      return linearVelocity/radius*180/pi
    else:
      return 0
    
#-------------------------------------------------------------------------------

  def getWheelRatesFromState(self, linearVelocity, steeringAngle):
    wheelRates = [0]*len(self.wheels)
    
    angularVelocity = self.getAngularVelocityFromState(linearVelocity,
      steeringAngle)
    for i in range(len(self.wheels)):
      wheelRates[i] = (((linearVelocity-self.getWheelTrack(i)*
        angularVelocity*pi/180)/self.wheelRadii[i])*180/pi)

    wheelAngles = self.getWheelAnglesFromSteeringAngle(steeringAngle)
    for i in [0, 1]:
      wheelRates[i] /= cos(wheelAngles[i]*pi/180)

    return wheelRates
    
#-------------------------------------------------------------------------------

  def isFrontWheel(self, wheel):
    return self.wheels.index(wheel) < 2

#-------------------------------------------------------------------------------

  def updateState(self, period):
    lastWheelAngles = self.wheelAngles
    
    d_v = self.command[0]-self.state[0]
    a_v = self.getAccelerationFromVelocities(self.state[0], self.command[0],
      self.maxAcceleration[0], self.maxDeceleration[0])
    if abs(a_v*period) > abs(d_v):
      self.state[0] = self.command[0]
    else:
      self.state[0] += a_v*period
    if abs(self.state[0]) > self.maxLinearVelocity:
      self.state[0] = signum(self.state[0])*self.maxLinearVelocity

    a_s = self.getAccelerationFromPositions(self.state[1], self.command[1],
      self.steeringRate, self.maxSteeringRate, self.maxAcceleration[1],
      self.maxDeceleration[1])
    self.steeringRate += a_s*period
    self.state[1] += self.steeringRate*period
    if abs(self.state[1]) > self.maxSteeringAngle:
      self.state[1] = signum(self.state[1])*self.maxSteeringAngle
    
    self.wheelRates = self.getWheelRatesFromState(
      self.state[0], self.state[1])
    
    self.wheelAngles = self.getWheelAnglesFromSteeringAngle(self.state[1])
    for i in [0, 1]:
      self.wheelSteeringRates[i] = (self.wheelAngles[i]-
        lastWheelAngles[i])/period
      
#-------------------------------------------------------------------------------

  def move(self, period):
    if abs(self.state[1]) >= self.epsilon:
      radius = self.wheelBase/tan(self.state[1]*pi/180)

      d_theta = self.state[0]*period/radius
      d_x = radius*sin(d_theta)
      d_y = radius*(1-cos(d_theta))
    else:
      d_theta = 0
      d_x = self.state[0]*period
      d_y = 0

    if self.actuated:
      self.actuated.x += (d_x*cos(self.actuated.yaw*pi/180)-
        d_y*sin(self.actuated.yaw*pi/180))
      self.actuated.y += (d_x*sin(self.actuated.yaw*pi/180)+
        d_y*cos(self.actuated.yaw*pi/180))
      self.actuated.yaw += d_theta*180/pi

    for i in [0, 1]:
      self.wheels[i].yaw += self.wheelSteeringRates[i]*period
        
    WheelDrive.move(self, period)
