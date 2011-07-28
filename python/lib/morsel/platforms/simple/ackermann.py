from morsel.core import *
from math import *
from morsel.platforms.ackermann import Ackermann as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Ackermann(Base):
  def __init__(self, world, name, mesh, chassisSolid = None, wheelSolid = None,
      **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.chassisSolid = Solid(name+"ChassisSolid", chassisSolid, self.chassis,
      parent = self)

    self.wheelSolids = []
    for wheel in self.wheels:
      self.wheelSolids.append(Solid(name+"WheelSolid", wheelSolid, wheel,
        parent = self))

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
    elif self.state[0] < -self.maxVelocity:
      self.state[0] = -self.maxVelocity;

    self.setRatesFromVelocities([self.state[0]]*4)
    self.steeringAngles = [self.state[1], self.state[1], 0, 0]

#-------------------------------------------------------------------------------

  def updatePose(self, period):
    if abs(self.state[1]) >= self.epsilon:
      radius = self.axesDistance/tan(self.state[1]*pi/180)

      dtheta = self.state[0]*period/radius
      dx = radius*sin(dtheta)
      dy = radius*(1-cos(dtheta))
    else:
      dtheta = 0
      dx = self.state[0]*period
      dy = 0

    self.pose[0] += dx*cos(self.pose[2]*pi/180)-dy*sin(self.pose[2]*pi/180)
    self.pose[1] += dx*sin(self.pose[2]*pi/180)+dy*cos(self.pose[2]*pi/180)
    self.pose[2] += dtheta*180/pi
