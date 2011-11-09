from morsel.panda import *
from morsel.math import *
from morsel.actuators import Accelerator as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Accelerator(Base):
  def __init__(self, world, name, mesh, solid = None, maxAcceleration = [0]*6,
      maxDeceleration = [0]*6, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration

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

    dt = panda.Vec3(*self.translationalVelocity)*period
    dr = panda.Vec3(*self.rotationalVelocity)*period
    dq = Quaternion()
    dq.setHpr(dr)

    self.position = (panda.Vec3(*self.position)+
      self.parent.getRelativeVector(self, dt))
    self.quaternion = self.globalQuaternion*dq
