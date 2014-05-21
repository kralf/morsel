from morsel.nodes.panda.facade import Solid
from morsel.sensors.inertial_sensor import InertialSensor as Base
from morsel.nodes.panda.sensor import Sensor

#-------------------------------------------------------------------------------

class InertialSensor(Sensor, Base):
  def __init__(self, solid = None, **kargs):
    super(InertialSensor, self).__init__(**kargs)

    self.solid = Solid(type = solid)
