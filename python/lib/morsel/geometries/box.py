from morsel.panda import *
from morsel.nodes.facade import Mesh
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Box(Geometry):
  def __init__(self, size = [1, 1, 1], **kargs):
    super(Box, self).__init__(**kargs)
    
    self.size = size

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:
      self._mesh = Mesh(filename = "geometry/cube.bam", parent = self)
      
    return self._mesh
    
  mesh = property(getMesh)

#-------------------------------------------------------------------------------

  def getSize(self, node = None):
    return self.getScale(node)
    
  def setSize(self, size, node = None):
    self.setScale(size, node)
    
  size = property(getSize, setSize)
  
#-------------------------------------------------------------------------------

  def getGlobalSize(self):
    return self.getSize(render)
    
  def setGlobalSize(self, size):
    self.setSize(size, render)
    
  globalSize = property(getGlobalSize, setGlobalSize)
  
#-------------------------------------------------------------------------------

  def getMinimun(self, node = None):
    if not node:
      node = self.parent
      
    p_min = node.getRelativePoint(self, panda.Point3(-0.5, -0.5, -0.5))
    
    return [p_min[0], p_min[1], p_min[2]]
    
  minimum = property(getMinimun)
  
#-------------------------------------------------------------------------------

  def getGlobalMinimum(self):
    return self.getMinimun(render)
    
  globalMinimum = property(getGlobalMinimum)
  
#-------------------------------------------------------------------------------

  def getMaximum(self, node = None):
    if not node:
      node = self.parent
    
    p_max = node.getRelativePoint(self, panda.Point3(0.5, 0.5, 0.5))
    
    return [p_max[0], p_max[1], p_max[2]]
    
  maximum = property(getMaximum)

#-------------------------------------------------------------------------------

  def getGlobalMaximum(self):
    return self.getMaximum(render)
    
  globalMaximum = property(getGlobalMaximum)
  