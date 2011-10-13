from morsel.core import *
from morsel.nodes.ode.geometry import Geometry

#-------------------------------------------------------------------------------

class Mesh(Geometry):
  def __init__(self, world, name, solid, mesh, **kargs):
    mesh.flattenLight()
    self.data = panda.OdeTriMeshData(mesh.getChild(0))
    geometry = panda.OdeTriMeshGeom(world.space, self.data)

    Geometry.__init__(self, world, name, solid, geometry = geometry, **kargs)
