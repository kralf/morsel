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

  def getTranslationalVelocity(self, node = None):
    if not node:
      node = self
      
    q = panda.Quat(self.solid.body.body.getQuaternion())
    rv = self.solid.body.body.getAngularVel()
    tv = self.world.scene.getQuaternion(node).xform(
      self.solid.body.body.getLinearVel()+
      rv.cross(-q.xform(self.solid.body.getPos())))

    return [tv[0], tv[1], tv[2]]

#-------------------------------------------------------------------------------

  def getRotationalVelocity(self, node = None):
    if not node:
      node = self

    rv = self.solid.body.body.getAngularVel()
    rv = self.world.scene.getQuaternion(node).xform(rv)*180.0/pi

    return [rv[2], rv[1], rv[0]]

#-------------------------------------------------------------------------------

  def updateVelocity(self, period):
    self.rotationalVelocity = self.getRotationalVelocity()
    self.translationalVelocity = self.getTranslationalVelocity()
