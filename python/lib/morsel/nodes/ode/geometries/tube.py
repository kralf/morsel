from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry

#-------------------------------------------------------------------------------

class Tube(Geometry):
  def __init__(self, world, name, solid, radius = 1, length = 1, **kargs):
    geometry = panda.OdeCappedCylinderGeom(world.space, radius, length)
    
    Geometry.__init__(self, world, name, solid, geometry = geometry, **kargs)
