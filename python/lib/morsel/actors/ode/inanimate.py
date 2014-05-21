from morsel.nodes.ode.facade import Solid, Body
from morsel.actors.inanimate import Inanimate as Base
from morsel.nodes.ode.actor import Actor

#-------------------------------------------------------------------------------

class Inanimate(Actor, Base):
  def __init__(self, solid = None, body = None, mass = 1, **kargs):
    super(Inanimate, self).__init__(**kargs)

    self.solid = Solid(type = solid)
    self.body = Body(type = body, mass = mass)
