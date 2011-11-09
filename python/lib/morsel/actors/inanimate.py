from morsel.nodes import Actor
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Inanimate(Actor):
  def __init__(self, world, name, mesh, **kargs):
    Actor.__init__(self, world, name, **kargs)

    self.mesh = mesh
    self.mesh.parent = self
