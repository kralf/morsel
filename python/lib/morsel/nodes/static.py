from morsel.world.globals import *
from node import Node
from morsel.nodes.facade import Collider, Solid, Mesh

#-------------------------------------------------------------------------------

class Static(Node):
  def __init__(self, world, name, mesh, solid = None, exclude = [], **kargs):
    Node.__init__(self, world, name, parent = world.scene, **kargs)

    self.mesh = Mesh(name = name+"Mesh", filename = mesh, exclude = exclude,
      parent = self)
 
    if solid:
      self.solid = Solid(name = name+"Solid", type = solid, mesh = self.mesh,
        parent = self.world.scene.solid)
    else:
      self.solid = Solid(name = name+"Solid", type = "Empty", mesh = self.mesh,
        parent = self.world.scene.solid)
