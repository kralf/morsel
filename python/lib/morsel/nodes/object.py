from morsel.panda import *
from node import Node

#-------------------------------------------------------------------------------

class Object(Node):
  def __init__(self, mesh = None, anchor = None, **kargs):
    self._mesh = None
    self._anchor = None
    
    super(Object, self).__init__(**kargs)

    self.mesh = mesh
    self.anchor = anchor

#-------------------------------------------------------------------------------

  def getMesh(self):
    return self._mesh
    
  def setMesh(self, mesh):
    if self._mesh:
      self._mesh.detachNode()
      
    self._mesh = mesh
    
    if self._mesh:
      self._mesh.parent = self
      self.applyTransform(self._mesh)
    
  mesh = property(getMesh, setMesh)

#-------------------------------------------------------------------------------

  def getAnchor(self):
    return self._anchor
    
  def setAnchor(self, anchor):
    self._anchor = anchor
    
    if self._anchor:
      self.parent = self._anchor
    
  anchor = property(getAnchor, setAnchor)
  