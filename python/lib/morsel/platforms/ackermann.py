from morsel.core import *
from math import *
from morsel.platforms import Wheeled

#-------------------------------------------------------------------------------

class Ackermann(Wheeled):
  def __init__(self, world, name, mesh, maxSteeringAngle = 0,
      maxSteeringRate = 0, maxVelocity = 0, maxAcceleration = 0,
      maxDeceleration = 0, epsilon = 1e-6, **kargs):
    self.maxSteeringAngle = maxSteeringAngle
    self.maxSteeringRate = maxSteeringRate
    self.maxVelocity = maxVelocity
    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration
    self.epsilon = epsilon
    
    self.pose = [0, 0, 0]
    limits = [(-maxVelocity, maxVelocity),
      (-maxSteeringAngle, maxSteeringAngle)]
      
    Wheeled.__init__(self, world, name, mesh, limits = limits, **kargs)

    self.axesDistance = 0.5*(self.getWheelDistance(0, 2)+
      self.getWheelDistance(1, 3))

#-------------------------------------------------------------------------------

  def setPosition(self, position):
    Wheeled.setPosition(self, position)
    self.pose[0] = position[0]
    self.pose[1] = position[1]

  position = property(Wheeled.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation):
    Wheeled.setOrientation(self, orientation)
    self.pose[2] = orientation[0]

  orientation = property(Wheeled.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def isFrontWheel(self, wheel):
    return self.wheels.index(wheel) < 2

#-------------------------------------------------------------------------------

  def updateState(self, period):
    if abs(self.state[1]-self.command[1]) < self.maxSteeringRate*period:
      self.state[1] = self.command[1]
    else:
      self.state[1] += (signum(self.command[1]-self.state[1])*
        self.maxSteeringRate*period)
    if self.state[1] > self.maxSteeringAngle:
      self.state[1] = self.maxSteeringAngle
    elif self.state[1] < - self.maxSteeringAngle:
      self.state[1] = -self.maxSteeringAngle

    dv = self.command[0]-self.state[0]
    if dv > -self.maxDeceleration*period and dv < self.maxAcceleration*period:
      self.state[0] = self.command[0]
    else:
      if dv < 0:
        self.state[0] -= self.maxDeceleration*period
      else:
        self.state[0] += self.maxAcceleration*period

    if self.state[0] > self.maxVelocity:
      self.state[0] = self.maxVelocity
    elif self.state[0] < 0:
      self.state[0] = 0

    self.setRatesFromVelocities([self.state[0]]*4)
    self.steeringAngles = [self.state[1], self.state[1], 0, 0]

#-------------------------------------------------------------------------------

  def updatePosition(self, period):
    if abs(self.state[1]) >= self.epsilon:
      radius = self.axesDistance/tan(self.state[1]*pi/180)
      dtheta = self.state[0]*period/radius
      
      dx = radius*sin(dtheta)
      dy = radius*(1-cos(dtheta))
    else:
      dx = self.state[0]*period
      dy = 0

    self.pose[0] += dx*cos(self.pose[2]*pi/180)-dy*sin(self.pose[2]*pi/180)
    self.pose[1] += dx*sin(self.pose[2]*pi/180)+dy*cos(self.pose[2]*pi/180)

#-------------------------------------------------------------------------------

  def updateOrientation(self, period):
    if abs(self.state[1]) >= self.epsilon:
      radius = self.axesDistance/tan(self.state[1]*pi/180)
      dtheta = self.state[0]*period/radius
    else:
      dtheta = 0

    self.pose[2] += dtheta*180/pi

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    self.updateState(period)

    self.updatePosition(period)
    self.updateOrientation(period)

    Wheeled.updatePhysics(self, period)
    
#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.setPosition([self.pose[0], self.pose[1], self.getZ()])
    self.setOrientation([self.pose[2], self.getP(), self.getR()])

    Wheeled.updateGraphics(self)
