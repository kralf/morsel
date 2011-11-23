from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Box(Geometry):
  def __init__(self, world, name, solid, scale = [1, 1, 1], **kargs):
    geometry = panda.OdeBoxGeom(world.space, *scale)

    Geometry.__init__(self, world, name, solid, geometry = geometry,
      scale = scale, **kargs)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(self.name+"Display", "geometry/cube.bam")
