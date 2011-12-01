from morsel.panda import *
from morsel.platforms import Wheeled as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Wheeled(Base):
  def __init__(self, world, name, mesh, bodySolid = None, **kargs):
    mesh = Mesh(name = name+"Mesh", filename = mesh)
    Base.__init__(self, world, name, mesh, **kargs)

    self.body.solid = Solid(name = name+"BodySolid", type = bodySolid,
      mesh = self, parent = self.chassis.solid)
    