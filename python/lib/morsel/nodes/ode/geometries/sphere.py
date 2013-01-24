from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Sphere(Geometry):
  def __init__(self, world, name, solid, **kargs):
    Geometry.__init__(self, world, name, solid, **kargs)

    self.scale = [max(self.scale)]*3
    radius = 0.5*max(self.globalScale)
    
    self.geometry = panda.OdeSphereGeom(world.space, radius)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(name = self.name+"Display", filename = "geometry/sphere.bam")
