from morsel.nodes.panda.facade import Solid
from morsel.actuators.drive import Drive as Base
from morsel.nodes.panda.actuator import Actuator

#-------------------------------------------------------------------------------

class Drive(Actuator, Base):
  def __init__(self, solid = None, **kargs):
    super(Drive, self).__init__(**kargs)        

    self.solid = Solid(type = solid)
    