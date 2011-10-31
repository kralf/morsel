from morsel.panda import *
from morsel.nodes.ode.solid import Solid
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Empty(Solid):
  def __init__(self, world, name, mesh = None, body = "Empty", **kargs):
    display = Mesh(name+"Display", "symbols/zup_axis.bam")
    
    Solid.__init__(self, world, name, mesh = mesh, body = body,
      display = display, scale = 0.1, **kargs)
