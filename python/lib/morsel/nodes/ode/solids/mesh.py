from morsel.core import *
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Mesh(Solid):
  def __init__(self, world, name, mesh, **kargs):
    mesh.flattenLight()
    
    self.data = panda.OdeTriMeshData(mesh.getChild(0))
    geometry = panda.OdeTriMeshGeom(world.space, self.data)

    Solid.__init__(self, world, name, mesh, geometry = geometry, **kargs)
