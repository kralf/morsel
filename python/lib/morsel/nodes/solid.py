from node import Node

#-------------------------------------------------------------------------------

class Solid(Node):
  def __init__(self, world, name, mesh, **kargs):
    Node.__init__(self, world, name, **kargs)
    
    self.mesh = mesh
