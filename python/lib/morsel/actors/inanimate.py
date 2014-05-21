from morsel.nodes.facade import Mesh
from morsel.nodes.actor import Actor

#-------------------------------------------------------------------------------

class Inanimate(Actor):
  def __init__(self, mesh = None, **kargs):
    super(Inanimate, self).__init__(**kargs)

    if mesh:
      self.mesh = Mesh(filename = mesh, flatten = True)
    