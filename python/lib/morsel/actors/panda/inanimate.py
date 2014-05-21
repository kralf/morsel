from morsel.nodes.panda.facade import Solid
from morsel.actors.inanimate import Inanimate as Base
from morsel.nodes.panda.actor import Actor

#-------------------------------------------------------------------------------

class Inanimate(Actor, Base):
  def __init__(self, solid = None, **kargs):
    super(Inanimate, self).__init__(**kargs)

    self.solid = Solid(type = solid)
    