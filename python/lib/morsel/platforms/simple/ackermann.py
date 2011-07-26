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
