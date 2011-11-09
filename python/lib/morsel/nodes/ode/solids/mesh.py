from morsel.panda import *
from morsel.nodes.ode.geometries import Mesh as Geometry
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Mesh(Solid):
  def __init__(self, world, name, mesh, **kargs):
    geometry = Geometry(world, name+"Geometry", self, mesh)

    Solid.__init__(self, world, name, mesh, geometry = geometry, **kargs)
