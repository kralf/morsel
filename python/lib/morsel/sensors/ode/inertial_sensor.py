from morsel.panda import *
from morsel.math import *
from morsel.sensors.inertial_sensor import InertialSensor as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class InertialSensor(Base):
  def __init__(self, world, name, mesh, solid = None, body = None, mass = 0,
      **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.solid = Solid(name = name+"Solid", type = solid, mesh = self.mesh,
      body = body, mass = mass, parent = self.parent.solid)
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.parent.solid.body.body, self.solid.body.body)
    joint.set()

#-------------------------------------------------------------------------------

  def updateVelocity(self, period):
    self.rotationalVelocity = self.solid.body.getRotationalVelocity(self)
    self.translationalVelocity = self.solid.body.getTranslationalVelocity(self)
    
    rv = panda.Vec3(self.rotationalVelocity[2], self.rotationalVelocity[1],
      self.rotationalVelocity[0])*pi/180.0
    tv = (panda.Vec3(*self.translationalVelocity)+
      rv.cross(-self.solid.body.getPos(self)))
    self.translationalVelocity = [tv[0], tv[1], tv[2]]
