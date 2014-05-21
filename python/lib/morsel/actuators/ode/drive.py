from morsel.nodes.ode.facade import Solid, Body
from morsel.actuators.drive import Drive as Base
from morsel.nodes.ode.actuator import Actuator

#-------------------------------------------------------------------------------

class Drive(Actuator, Base):
  def __init__(self, solid = None, body = None, mass = 1, **kargs):
    super(Drive, self).__init__(**kargs)

    self.solid = Solid(type = solid)
    self.body = Body(type = body, mass = mass)
    