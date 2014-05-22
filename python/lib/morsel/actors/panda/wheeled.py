from morsel.nodes.panda.facade import Solid
from morsel.actors.wheeled import Wheeled as Base
from morsel.nodes.panda.actor import Actor

#-------------------------------------------------------------------------------

class Wheeled(Actor, Base):
  def __init__(self, bodySolid = None, **kargs):
    super(Wheeled, self).__init__(**kargs)
    
    self.actuator.stash()
    self.solid = Solid(type = bodySolid)
    self.actuator.unstash()
