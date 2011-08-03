from morsel.core import *
from math import *
from morsel.platforms import Wheeled

#-------------------------------------------------------------------------------

class Ackermann(Wheeled):
  def __init__(self, world, name, mesh, maxSteeringAngle = 0, maxVelocity = 0,
      epsilon = 1e-6, **kargs):
    self.maxSteeringAngle = maxSteeringAngle
    self.maxVelocity = maxVelocity
    self.epsilon = epsilon
    
    limits = [(-maxVelocity, maxVelocity),
      (-maxSteeringAngle, maxSteeringAngle)]
    Wheeled.__init__(self, world, name, mesh, limits = limits, **kargs)

    self.wheelDistance = self.getWheelDistance(0, 1)
    self.axesDistance = 0.5*(self.getWheelDistance(0, 2)+
      self.getWheelDistance(1, 3))

#-------------------------------------------------------------------------------

  def getSteeringAngles(self, steeringAngle):
    steeringAngles = [0]*self.numWheels
    
    if tan(steeringAngle*pi/180) == 0:
      return steeringAngles
      
    cotLeftAngle = (1/tan(steeringAngle*pi/180)+
      self.wheelDistance/(2*self.axesDistance))
    cotRightAngle = cotLeftAngle-self.wheelDistance/self.axesDistance
    
    steeringAngles[0] = atan(1/cotLeftAngle)*180/pi
    steeringAngles[1] = atan(1/cotRightAngle)*180/pi
    
    return steeringAngles

#-------------------------------------------------------------------------------

  def isFrontWheel(self, wheel):
    return self.wheels.index(wheel) < 2
