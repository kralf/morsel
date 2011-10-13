from morsel.core import *
from morsel.nodes.ode.geometry import Geometry

#-------------------------------------------------------------------------------

class Box(Geometry):
  def __init__(self, world, name, solid, length = [1, 1, 1], **kargs):
    geometry = panda.OdeBoxGeom(world.space, *length)
    
    Geometry.__init__(self, world, name, solid, geometry = geometry, **kargs)
  