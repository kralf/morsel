from morsel.nodes import Actor
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Inanimate(Actor):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    Actor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)
    self.solid = Solid(name+"Solid", "Empty", parent = self)
    self.boundingSolid = Solid(name+"Solid", solid, self.mesh,
      parent = self.solid)
