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
    pass

#-------------------------------------------------------------------------------

  def updatePose(self, period):
    pass

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    self.updateState(period)
    self.updatePose(period)

    Wheeled.updatePhysics(self, period)
    
#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.setPosition([self.pose[0], self.pose[1], self.getZ()])
    self.setOrientation([self.pose[2], self.getP(), self.getR()])

    Wheeled.updateGraphics(self)
