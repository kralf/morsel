from morsel.actors import Character as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Character(Base):
  def __init__(self, world, name, mesh, bodySolid = None, **kargs):
    mesh = Mesh(name = name+"Mesh", filename = mesh)
    Base.__init__(self, world, name, mesh, **kargs)

    if self.body:
      self.body.solid = Solid(name = name+"BodySolid", type = bodySolid,
        mesh = self, parent = self.motor.solid)
    