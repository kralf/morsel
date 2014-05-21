from morsel.panda import *
from morsel.nodes.node import Node
from morsel.nodes.ode.object import Object
from morsel.nodes.facade import Mesh as _Mesh
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Mesh(Solid):
  def __init__(self, **kargs):
    super(Mesh, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh and self.object:
      self._mesh = _Mesh(parent = self)
      self._mesh.copyFrom(self.object.mesh.model, flatten = True)
            
    return self._mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def fit(self, node):
    Solid.fit(self, node)
    
    mesh = _Mesh(position = self.globalPosition, orientation =
      self.globalOrientation)
    mesh.copyFrom(node.mesh, flatten = True)
    data = panda.OdeTriMeshData(mesh)
    mesh.detachNode()
    
    self.geometry = panda.OdeTriMeshGeom(node.world.space, data)
  