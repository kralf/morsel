from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Empty(Geometry):
  def __init__(self, world, name, solid, scale = [1, 1, 1], **kargs):
    Geometry.__init__(self, world, name, solid, **kargs)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(name = self.name+"Display", filename = "symbols/zup_axis.bam",
      scale = [0.1]*3)
    