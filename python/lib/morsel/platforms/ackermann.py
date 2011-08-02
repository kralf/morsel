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

    self.axesDistance = 0.5*(self.getWheelDistance(0, 2)+
      self.getWheelDistance(1, 3))

#-------------------------------------------------------------------------------

  def isFrontWheel(self, wheel):
    return self.wheels.index(wheel) < 2
