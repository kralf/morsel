from morsel.core import *
from morsel.nodes.simple.solid import Solid
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Empty(Solid):
  def __init__(self, world, name, mesh = None, **kargs):
    Solid.__init__(self, world, name, mesh = mesh, **kargs)
    
    self.display = Mesh(name+"Display", "symbols/zup_axis.bam",
      scale = 0.1, color = [1, 1, 1, 0.5], parent = self)
    self.display.flattenStrong()
    