from morsel.panda import *
from morsel.math import *
from morsel.nodes import Sensor
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class InertialSensor(Sensor):
  def __init__(self, world, name, mesh, **kargs):
    Sensor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name = name+"Mesh", filename = mesh, parent = self)

    self.timestamp = 0.0
    self.translationalVelocity = [0, 0, 0]
    self.rotationalVelocity = [0, 0, 0]
    self.translationalAcceleration = [0, 0, 0]
    self.rotationalAcceleration = [0, 0, 0]

    self.lastTranslationalVelocity = None
    self.lastRotationalVelocity = None

#-------------------------------------------------------------------------------

  def getTranslationalVelocity(self, node = None):
    if not node:
      node = self

    tv = panda.Vec3(*self.translationalVelocity)
    tv = self.getQuaternion(node).xform(tv)

    return [tv[0], tv[1], tv[2]]

#-------------------------------------------------------------------------------

  def getRotationalVelocity(self, node = None):
    if not node:
      node = self

    rv = panda.Vec3(self.rotationalVelocity[2], self.rotationalVelocity[1],
      self.rotationalVelocity[0])
    rv = self.getQuaternion(node).xform(rv)

    return [rv[2], rv[1], rv[0]]

#-------------------------------------------------------------------------------

  def updateVelocity(self, period):
    pass
  
#-------------------------------------------------------------------------------

  def updateAcceleration(self, period):
    if self.lastTranslationalVelocity:
      ta = ((panda.Vec3(*self.translationalVelocity)-
        panda.Vec3(*self.lastTranslationalVelocity))/period)
      self.translationalAcceleration = [ta[0], ta[1], ta[2]]
    if self.lastRotationalVelocity:
      ra = ((panda.Vec3(*self.rotationalVelocity)-
        panda.Vec3(*self.lastRotationalVelocity))/period)
      self.rotationalAcceleration = [ra[0], ra[1], ra[2]]

    self.lastTranslationalVelocity = self.translationalVelocity
    self.lastRotationalVelocity = self.rotationalVelocity

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    self.updateVelocity(period)
    self.updateAcceleration(period)

    self.timestamp = self.world.time
    