from morsel.panda import *
from morsel.math import *
from morsel.actuators import Ackermann as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Ackermann(Base):
  def __init__(self, world, name, mesh, wheelSolid = None, maxSteeringRate = 0,
      maxAcceleration = 0, maxDeceleration = 0, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.maxSteeringRate = maxSteeringRate
    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration

    self.wheelSolids = []
    for wheel in self.wheels:
      self.wheelSolids.append(Solid(name+"WheelSolid", wheelSolid, wheel,
        parent = self.solid))

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
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
    if (dv > -self.maxDeceleration*period) and \
        (dv < self.maxAcceleration*period):
      self.state[0] = self.command[0]
    else:
      if dv < 0:
        self.state[0] -= self.maxDeceleration*period
      else:
        self.state[0] += self.maxAcceleration*period

    if self.state[0] > self.maxVelocity:
      self.state[0] = self.maxVelocity
    elif self.state[0] < -self.maxVelocity:
      self.state[0] = -self.maxVelocity;

    self.setRatesFromVelocities([self.state[0]]*4)
    self.steeringAngles = [self.state[1], self.state[1], 0, 0]

    if abs(self.state[1]) >= self.epsilon:
      radius = self.steeringAxisDistance/tan(self.state[1]*pi/180)

      dtheta = self.state[0]*period/radius
      dx = radius*sin(dtheta)
      dy = radius*(1-cos(dtheta))
    else:
      dtheta = 0
      dx = self.state[0]*period
      dy = 0

    self.x += dx*cos(self.yaw*pi/180)-dy*sin(self.yaw*pi/180)
    self.y += dx*sin(self.yaw*pi/180)+dy*cos(self.yaw*pi/180)
    self.yaw += dtheta*180/pi

    Base.updatePhysics(self, period)
