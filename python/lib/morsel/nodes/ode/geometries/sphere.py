from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry

#-------------------------------------------------------------------------------

class Sphere(Geometry):
  def __init__(self, world, name, solid, radius = 1, **kargs):
    geometry = panda.OdeSphereGeom(world.space, radius)

    Geometry.__init__(self, world, name, solid, geometry = geometry, **kargs)
