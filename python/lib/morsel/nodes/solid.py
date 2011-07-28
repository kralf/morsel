from node import Node
from facade import Collider

#-------------------------------------------------------------------------------

class Solid(Node):
  def __init__(self, world, name, mesh, parent = None, **kargs):
    if not parent.collider:
      parent.collider = Collider(parent.name+"Collider", parent = parent)

    Node.__init__(self, world, name, parent = parent.collider, **kargs)
    parent.collider.addSolid(self)

    self.mesh = mesh
