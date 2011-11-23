from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Sphere(Geometry):
  def __init__(self, world, name, solid, scale = [1, 1, 1], **kargs):
    radius = 0.5*max(scale)
    geometry = panda.OdeSphereGeom(world.space, radius)

    Geometry.__init__(self, world, name, solid, geometry = geometry,
      scale = [2*radius]*3, **kargs)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(self.name+"Display", "geometry/sphere.bam")
