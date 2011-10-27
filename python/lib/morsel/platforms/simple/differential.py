from morsel.core import *
from math import *
from morsel.platforms.differential import Differential as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Differential(Base):
  def __init__(self, world, name, mesh, chassisSolid = None, wheelSolid = None,
      crankSolid = None, maxAcceleration = 0, maxDeceleration = 0, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration

    self.solid = Solid(name+"Solid", "Empty", parent = self)
    self.chassisSolid = Solid(name+"ChassisSolid", chassisSolid, self.chassis,
      parent = self.solid)

    self.crankSolids = []
    for crank in self.casterCranks:
      self.crankSolids.append(Solid(name+"CrankSolid", crankSolid, crank,
        parent = self.chassisSolid))
        
    self.wheelSolids = []
    for wheel in self.wheels:
      self.wheelSolids.append(Solid(name+"WheelSolid", wheelSolid, wheel,
        parent = self.chassisSolid))

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    if abs(self.state[1]-self.command[1]) < self.maxRotationalVelocity*period:
      self.state[1] = self.command[1]
    else:
      self.state[1] += (signum(self.command[1]-self.state[1])*
        self.maxRotationalVelocity*period)
    if self.state[1] > self.maxRotationalVelocity:
      self.state[1] = self.maxRotationalVelocity
    elif self.state[1] < - self.maxRotationalVelocity:
      self.state[1] = -self.maxRotationalVelocity

    dv = self.command[0]-self.state[0]
    if dv > -self.maxDeceleration*period and dv < self.maxAcceleration*period:
      self.state[0] = self.command[0]
    else:
      if dv < 0:
        self.state[0] -= self.maxDeceleration*period
      else:
        self.state[0] += self.maxAcceleration*period

    if self.state[0] > self.maxTranslationalVelocity:
      self.state[0] = self.maxTranslationalVelocity
    elif self.state[0] < -self.maxTranslationalVelocity:
      self.state[0] = -self.maxTranslationalVelocity;

    dtheta = self.state[1]*pi/180*period
    dx = self.state[0]*cos(dtheta)*period
    dy = self.state[0]*sin(dtheta)*period

    casterRates = self.getCasterRates(self.state[0], self.state[1])
    for i in range(self.numCasters):
      self.casterAngles[i] += casterRates[i]*period
    self.turningRates = self.getTurningRates(self.state[0], self.state[1])

    self.pose[0] += dx*cos(self.pose[3]*pi/180)-dy*sin(self.pose[3]*pi/180)
    self.pose[1] += dx*sin(self.pose[3]*pi/180)+dy*cos(self.pose[3]*pi/180)
    self.pose[3] += dtheta*180/pi

    Base.updatePhysics(self, period)
    