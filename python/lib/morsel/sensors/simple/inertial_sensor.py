from morsel.sensors.inertial_sensor import InertialSensor as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class InertialSensor(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.solid = Solid(name = name+"Solid", type = solid, mesh = self.mesh,
      parent = self)

    self.lastPosition = None
    self.lastOrientation = None

#-------------------------------------------------------------------------------

  def updateVelocity(self, period):
    if self.lastPosition:
      tv = ((panda.Vec3(*self.globalPosition)-
        panda.Vec3(*self.lastPosition))/period)
      tv = self.getRelativeVector(self.world.scene, tv)
      self.translationalVelocity = [tv[0], tv[1], tv[2]]
    if self.lastOrientation:
      rv = ((panda.Vec3(*self.globalOrientation)-
        panda.Vec3(*self.lastOrientation))/period)
      rv = self.getRelativeVector(self.world.scene,
        panda.Vec3(rv[2], rv[1], rv[0]))
      self.rotationalVelocity = [rv[2], rv[1], rv[0]]

    self.lastPosition = self.globalPosition
    self.lastOrientation = self.globalOrientation
