from globals import *
from object import Object
from morsel.nodes.facade import Collider, Solid, Mesh

#-------------------------------------------------------------------------------

class Static(Object):
  def __init__(self, world, name, mesh, exclude = [], **kargs):
    Object.__init__(self, world, name, parent = world.scene, **kargs)

    self.mesh = Mesh(name = name+"Mesh", filename = mesh, exclude = exclude,
      parent = self)
    