from morsel.nodes.solid import Solid as Base
from morsel.nodes.simple.collider import Collider

#-------------------------------------------------------------------------------

class Solid(Base):
  def __init__(self, world, name, mesh, geometry = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    if not isinstance(self.parent, Collider):
      if not self.parent.collider:
        self.parent.collider = Collider(world, self.parent.name+"Collider",
          parent = self.parent)
      self.parent = self.parent.collider

    self.geometry = geometry    
    if self.geometry:
      self.parent.addSolid(self)
