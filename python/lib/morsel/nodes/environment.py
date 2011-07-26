from node import Node
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Environment(Node):
  def __init__(self, world, name, mesh, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)
    