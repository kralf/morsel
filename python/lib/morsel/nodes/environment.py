from morsel.world.globals import *
from node import Node
from morsel.nodes.facade import Collider, Mesh

#-------------------------------------------------------------------------------

class Environment(Node):
  def __init__(self, world, name, mesh, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.collider = Collider(name+"Collider", parent = self,
      collisionMasks = [STATIC_COLLISIONS_FROM, STATIC_COLLISIONS_INTO])

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)
    