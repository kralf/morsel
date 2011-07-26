from morsel.nodes.environment import Environment as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Environment(Base):
  def __init__(self, world, name, mesh, solid = "Mesh", **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.solid = None
    if solid:
      self.solid = Solid(name+"Solid", solid, self.mesh, parent = self)
