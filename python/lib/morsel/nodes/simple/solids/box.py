from morsel.core import *
from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Box(Solid):
  def __init__(self, world, name, mesh, **kargs):
    p_min, p_max = mesh.getTightBounds()
    geometry = panda.CollisionBox(p_min, p_max)

    Solid.__init__(self, world, name, mesh, geometry, **kargs)
