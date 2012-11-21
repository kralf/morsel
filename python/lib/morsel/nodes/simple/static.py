from morsel.panda import *
from morsel.nodes.static import Static as Base

#-------------------------------------------------------------------------------

class Static(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    if not solid:
      solid = "Empty"
      
    self.solid = Solid(name = name+"Solid", type = solid, mesh = self.mesh,
      parent = self)
