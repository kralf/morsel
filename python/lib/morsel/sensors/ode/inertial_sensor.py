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
    rv = self.solid.body.body.getAngularVel()
    tv = self.world.scene.getQuaternion(self).xform(
      self.solid.body.body.getLinearVel()+
      rv.cross(self.getPos(self.world.scene)-
      self.solid.body.getPos(self.world.scene)))
    
    self.rotationalVelocity = self.solid.body.getRotationalVelocity(self)
    self.translationalVelocity = [tv[0], tv[1], tv[2]]
