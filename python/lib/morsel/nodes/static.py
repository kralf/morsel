from morsel.world.globals import *
from node import Node
from morsel.nodes.facade import Collider, Solid, Mesh

#-------------------------------------------------------------------------------

class Static(Node):
  def __init__(self, world, name, mesh, solid = None, exclude = [], **kargs):
    Node.__init__(self, world, name, **kargs)

    self.collider = Collider(name+"Collider", parent = self,
      collisionMasks = [STATIC_COLLISIONS_FROM, STATIC_COLLISIONS_INTO])
    self.solid = None
    
    self.mesh = Mesh(name+"Mesh", mesh, exclude = exclude, parent = self)
    if solid:
      self.solid = Solid(name+"Solid", solid, self.mesh, parent = self)
