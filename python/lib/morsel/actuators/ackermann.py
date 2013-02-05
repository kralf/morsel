from morsel.panda import *
from morsel.math import *
from morsel.actuators import WheelChassis

#-------------------------------------------------------------------------------

class Ackermann(WheelChassis):
  def __init__(self, world, name, mesh, maxSteeringAngle = 0, maxVelocity = 0,
      epsilon = 1e-6, **kargs):
    self.maxSteeringAngle = maxSteeringAngle
    self.maxVelocity = maxVelocity
    self.epsilon = epsilon
    
    limits = [(-maxVelocity, maxVelocity),
      (-maxSteeringAngle, maxSteeringAngle)]      
    WheelChassis.__init__(self, world, name, mesh, limits = limits, **kargs)

#-------------------------------------------------------------------------------

  def getSteeringWheelDistance(self):
    return self.getWheelDistance(0, 1)

  steeringWheelDistance = property(getSteeringWheelDistance)

#-------------------------------------------------------------------------------

  def getSteeringAxisDistance(self):
    return 0.5*(self.getWheelDistance(0, 2)+
      self.getWheelDistance(1, 3))

  steeringAxisDistance = property(getSteeringAxisDistance)

#-------------------------------------------------------------------------------

  def getSteeringAngle(self, steeringAngles):
    steeringAngle = 0
    
    if ((tan(steeringAngles[0]*pi/180) == 0) or 
        tan(steeringAngles[1]*pi/180) == 0):
      return steeringAngle

    cotLeftAngle = 1/tan(steeringAngles[0]*pi/180)
    cotRightAngle = 1/tan(steeringAngles[1]*pi/180)
    
    leftSteeringAngle = atan(1/(cotLeftAngle-self.steeringWheelDistance/
      (2*self.steeringAxisDistance)))*180/pi
    rightSteeringAngle = atan(1/(cotRightAngle+self.steeringWheelDistance/
      (2*self.steeringAxisDistance)))*180/pi

    return 0.5*(leftSteeringAngle+rightSteeringAngle)

#-------------------------------------------------------------------------------

  def getSteeringAngles(self, steeringAngle):
    steeringAngles = [0]*self.numWheels
    
    if tan(steeringAngle*pi/180) == 0:
      return steeringAngles
      
    cotLeftAngle = (1/tan(steeringAngle*pi/180)+
      self.steeringWheelDistance/(2*self.steeringAxisDistance))
    cotRightAngle = (cotLeftAngle-self.steeringWheelDistance/
      self.steeringAxisDistance)
    
    steeringAngles[0] = atan(1/cotLeftAngle)*180/pi
    steeringAngles[1] = atan(1/cotRightAngle)*180/pi
    
    return steeringAngles

#-------------------------------------------------------------------------------

  def getTranslationalVelocity(self):
    return [self.state[0], 0, 0]

  def setTranslationalVelocity(self, translationalVelocity):
    self.command = [translationalVelocity[0], self.command[1]]

  translationalVelocity = property(getTranslationalVelocity,
    setTranslationalVelocity)

#-------------------------------------------------------------------------------

  def getRotationalVelocity(self):
    if abs(self.state[1]) >= self.epsilon:
      radius = self.steeringAxisDistance/tan(self.state[1]*pi/180)
      return [self.state[0]/radius*180/pi, 0, 0]
    else:
      return [0, 0, 0]

  def setRotationalVelocity(self, rotationalVelocity):
    if abs(rotationalVelocity[0]) >= self.epsilon:
      radius = self.command[0]/(rotationalVelocity[0]*pi/180)
      if abs(radius) >= self.epsilon:
        self.command = [self.command[0],
          atan(self.steeringAxisDistance/radius)*180/pi]
    else:
      self.command = [self.command[0], 0]

  rotationalVelocity = property(getRotationalVelocity, setRotationalVelocity)

#-------------------------------------------------------------------------------

  def isFrontWheel(self, wheel):
    return self.wheels.index(wheel) < 2
