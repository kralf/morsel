from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Ray(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      scale = [1, 1, 1], **kargs):
    geometry = panda.OdeRayGeom(world.space, scale[2])

    position[2] -= 0.5*scale[2]
    Geometry.__init__(self, world, name, solid, geometry = geometry,
      position = position, scale = [1, 1, scale[2]], **kargs)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(self.name+"Display", "geometry/cylinder.bam",
      position = [0, 0, 0.5*self.geometry.getLength()],
      scale = [0.01, 0.01, 1])
