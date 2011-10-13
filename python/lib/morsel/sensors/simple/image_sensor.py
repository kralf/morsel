from morsel.sensors.image_sensor import ImageSensor as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class ImageSensor(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.solid = Solid(name+"Solid", solid, self.mesh, parent = self)
