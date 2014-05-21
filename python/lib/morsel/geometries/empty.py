from morsel.panda import *
from morsel.nodes.facade import Mesh
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Empty(Geometry):
  def __init__(self, **kargs):
    super(Empty, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:      
      self._mesh = Mesh(filename = "symbols/zup_axis.bam", parent = self)      
      self.onScale([1, 1, 1])
      
    return self._mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def fit(self, node):
    self.clearTransform(node)
    
#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self._mesh:
      scale = 0.1*max(self.scale)
      
      self._mesh.scale = [scale/self.scale[0], scale/self.scale[1],
        scale/self.scale[2]]
      