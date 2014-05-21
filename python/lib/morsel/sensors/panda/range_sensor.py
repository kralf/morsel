from morsel.nodes.panda.facade import Solid
from morsel.sensors.range_sensor import RangeSensor as Base
from morsel.nodes.panda.sensor import Sensor

#-------------------------------------------------------------------------------

class RangeSensor(Sensor, Base):
  def __init__(self, solid = None, **kargs):
    super(RangeSensor, self).__init__(**kargs)

    self.solid = Solid(type = solid)
