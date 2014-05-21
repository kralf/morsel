from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.sensor import Sensor

#-------------------------------------------------------------------------------

class InertialSensor(Sensor):
  def __init__(self, mesh = None, **kargs):
    super(InertialSensor, self).__init__(**kargs)

    if mesh:
      self.mesh = Mesh(filename = mesh, flatten = True)

    self.timestamp = 0.0
    self.linearVelocity = [0, 0, 0]
    self.angularVelocity = [0, 0, 0]
    self.linearAcceleration = [0, 0, 0]
    self.angularAcceleration = [0, 0, 0]

    self.lastPosition = None
    self.lastOrientation = None
    self.lastLinearVelocity = None
    self.lastAngularVelocity = None

#-------------------------------------------------------------------------------

  def getLinearVelocity(self, node = None):
    if not node:
      node = self

    v = panda.Vec3(*self.linearVelocity)
    v = self.getQuaternion(node).xform(v)

    return [v[0], v[1], v[2]]

#-------------------------------------------------------------------------------

  def getAngularVelocity(self, node = None):
    if not node:
      node = self

    omega = panda.Vec3(self.angularVelocity[2], self.angularVelocity[1],
      self.angularVelocity[0])
    omega = self.getQuaternion(node).xform(omega)

    return [omega[2], omega[1], omega[0]]

#-------------------------------------------------------------------------------

  def updateVelocity(self, period):
    if self.lastPosition:
      v = ((panda.Vec3(*self.globalPosition)-
        panda.Vec3(*self.lastPosition))/period)
      v = self.world.scene.getQuaternion(self).xform(v)
      self.linearVelocity = [v[0], v[1], v[2]]
    if self.lastOrientation:
      omega = ((panda.Vec3(*self.globalOrientation)-
        panda.Vec3(*self.lastOrientation))/period)
      omega = panda.Vec3(omega[2], omega[1], omega[0])
      omega = self.world.scene.getQuaternion(self).xform(omega)
      self.angulawelocity = [omega[2], omega[1], omega[0]]

    self.lastPosition = self.globalPosition
    self.lastOrientation = self.globalOrientation
  
#-------------------------------------------------------------------------------

  def updateAcceleration(self, period):
    if self.lastLinearVelocity:
      a = ((panda.Vec3(*self.linearVelocity)-
        panda.Vec3(*self.lastLinearVelocity))/period)
      self.linearAcceleration = [a[0], a[1], a[2]]
    if self.lastAngularVelocity:
      alpha = ((panda.Vec3(*self.angularVelocity)-
        panda.Vec3(*self.lastAngularVelocity))/period)
      self.angularAcceleration = [alpha[0], alpha[1], alpha[2]]

    self.lastLinearVelocity = self.linearVelocity
    self.lastAngularVelocity = self.angularVelocity

#-------------------------------------------------------------------------------

  def step(self, period):
    self.updateVelocity(period)
    self.updateAcceleration(period)

    self.timestamp = self.world.time
    