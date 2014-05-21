from morsel.nodes.panda.facade import Solid
from morsel.actuators.motor import Motor as Base
from morsel.nodes.panda.actuator import Actuator

#-------------------------------------------------------------------------------

class Motor(Actuator, Base):
  def __init__(self, solid = None, **kargs):
    super(Motor, self).__init__(**kargs)        

    self.solid = Solid(type = solid)
