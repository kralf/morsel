from morsel.core import *
from morsel.nodes import Actor
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Inanimate(Actor):
  def __init__(self, world, name, mesh, solid = None, body = None, mass = 0,
      **kargs):
    Actor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)
    self.solid = None

    if solid:
      self.solid = Solid(name+"Solid", solid, self.mesh, body = body,
        mass = mass, parent = self)
