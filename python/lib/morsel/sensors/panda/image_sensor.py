from morsel.nodes.panda.facade import Solid
from morsel.sensors.image_sensor import ImageSensor as Base
from morsel.nodes.panda.sensor import Sensor

#-------------------------------------------------------------------------------

class ImageSensor(Sensor, Base):
  def __init__(self, solid = None, **kargs):
    super(ImageSensor, self).__init__(**kargs)

    self.solid = Solid(type = solid)
