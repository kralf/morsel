from morsel.core import *
from morsel.nodes import Actor
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Inanimate(Actor):
  def __init__(self, world, name, mesh, **kargs):
    Actor.__init__(self, world, name, **kargs)

    self.body = Mesh(name+"Body", mesh, parent = self)
