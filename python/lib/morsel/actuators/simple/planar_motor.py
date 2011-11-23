from morsel.panda import *
from morsel.math import *
from morsel.actuators import PlanarMotor as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class PlanarMotor(Base):
  def __init__(self, world, name, mesh, baseSolid = None,
      maxAcceleration = [0, 0, 0], maxDeceleration = [0, 0, 0], **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration

    self.baseSolid = Solid(name+"BaseSolid", baseSolid, self.base,
      parent = self.solid)
        
#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    for i in range(0, len(self.state)):
      dv = self.command[i]-self.state[i]
      if (dv > -self.maxDeceleration[i]*period) and \
          (dv < self.maxAcceleration[i]*period):
        self.state[i] = self.command[i]
      else:
        if dv < 0:
          self.state[i] -= self.maxDeceleration[i]*period
        else:
          self.state[i] += self.maxAcceleration[i]*period

    dx = self.translationalVelocity[0]*period
    dy = self.translationalVelocity[1]*period
    dtheta = self.rotationalVelocity*period
    dquat = Quaternion()
    dquat.setHpr(panda.Vec3(dtheta, 0, 0))

    self.position = (panda.Vec3(*self.position)+
      self.parent.getRelativeVector(self, panda.Vec3(dx, dy, 0)))
    self.quaternion = self.globalQuaternion*dquat
