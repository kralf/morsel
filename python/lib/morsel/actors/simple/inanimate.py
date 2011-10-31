from morsel.actors import Inanimate as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Inanimate(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.body.solid = Solid(name+"Solid", solid, self.body,
      parent = self.solid)
