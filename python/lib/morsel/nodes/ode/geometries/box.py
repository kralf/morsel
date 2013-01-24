from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Box(Geometry):
  def __init__(self, world, name, solid, **kargs):
    Geometry.__init__(self, world, name, solid, **kargs)

    self.geometry = panda.OdeBoxGeom(world.space, *self.globalScale)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(name = self.name+"Display", filename = "geometry/cube.bam")
