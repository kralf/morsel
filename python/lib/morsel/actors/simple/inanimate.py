from morsel.actors import Inanimate as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Inanimate(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    mesh = Mesh(name+"Mesh", mesh)
    Base.__init__(self, world, name, mesh, **kargs)

    self.mesh.solid = Solid(name+"Solid", solid, self.mesh,
      parent = self.solid)
