from morsel.nodes.ode.facade import Solid, Body
from morsel.sensors.image_sensor import ImageSensor as Base
from morsel.nodes.ode.sensor import Sensor

#-------------------------------------------------------------------------------

class ImageSensor(Sensor, Base):
  def __init__(self, solid = None, body = None, mass = 1, **kargs):
    super(ImageSensor, self).__init__(**kargs)

    self.solid = Solid(type = solid)
    self.body = Body(type = body, mass = mass)
  