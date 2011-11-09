from morsel.actors import Animate as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Animate(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    mesh = Mesh(name+"Mesh", mesh)
    Base.__init__(self, world, name, mesh, **kargs)

    self.mesh.solid = Solid(name+"Solid", solid, self.mesh,
      parent = self.solid)
    