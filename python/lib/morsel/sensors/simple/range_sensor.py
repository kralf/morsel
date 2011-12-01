from morsel.sensors.range_sensor import RangeSensor as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class RangeSensor(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.solid = Solid(name = name+"Solid", type = solid, mesh = self.mesh,
      parent = self)
