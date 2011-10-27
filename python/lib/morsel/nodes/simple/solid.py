from morsel.nodes.solid import Solid as Base
from morsel.nodes.simple.collider import Collider

#-------------------------------------------------------------------------------

class Solid(Base):
  def __init__(self, world, name, mesh = None, geometry = None, **kargs):
    self.geometry = geometry

    Base.__init__(self, world, name, mesh = mesh, **kargs)
