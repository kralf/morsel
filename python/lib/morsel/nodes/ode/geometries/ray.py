from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Ray(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      scale = [1, 1, 1], **kargs):
    position[2] -= 0.5*scale[2]
    Geometry.__init__(self, world, name, solid, position = position,
      scale = [1, 1, scale[2]], **kargs)
    
    self.geometry = panda.OdeRayGeom(world.space, self.globalScale[2])

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(name = self.name+"Display", filename = "geometry/cylinder.bam",
      position = [0, 0, 0.5*self.geometry.getLength()],
      scale = [0.01, 0.01, 1])
