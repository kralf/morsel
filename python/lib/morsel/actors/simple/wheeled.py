from morsel.actors import Wheeled as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Wheeled(Base):
  def __init__(self, world, name, mesh, bodySolid = None, **kargs):
    mesh = Mesh(name+"Mesh", mesh)
    Base.__init__(self, world, name, mesh, **kargs)

    if self.body:
      self.body.solid = Solid(name+"BodySolid", bodySolid, self,
        parent = self.chassis.solid)
    