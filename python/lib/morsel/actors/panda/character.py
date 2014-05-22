from morsel.nodes.panda.facade import Solid
from morsel.actors.character import Character as Base
from morsel.nodes.panda.actor import Actor

#-------------------------------------------------------------------------------

class Character(Actor, Base):
  def __init__(self, bodySolid = None, **kargs):
    super(Character, self).__init__(**kargs)
    
    self.actuator.stash()
    self.solid = Solid(type = bodySolid)
    self.actuator.unstash()
    