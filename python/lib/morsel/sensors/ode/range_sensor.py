from morsel.nodes.ode.facade import Solid, Body
from morsel.sensors.range_sensor import RangeSensor as Base
from morsel.nodes.ode.sensor import Sensor

#-------------------------------------------------------------------------------

class RangeSensor(Sensor, Base):
  def __init__(self, solid = None, body = None, mass = 1, **kargs):
    super(RangeSensor, self).__init__(**kargs)

    self.solid = Solid(type = solid)
    self.body = Body(type = body, mass = mass)
    