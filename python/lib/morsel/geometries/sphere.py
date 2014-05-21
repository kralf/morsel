from morsel.panda import *
from morsel.nodes.facade import Mesh
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Sphere(Geometry):
  def __init__(self, radius = 0.5, **kargs):
    super(Sphere, self).__init__(**kargs)
    
    self.radius = radius

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:
      self._mesh = Mesh(filename = "geometry/sphere.bam", parent = self)
      
    return self._mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def getRadius(self, node = None):
    return 0.5*max(self.getScale(node))
    
  def setRadius(self, radius, node = None):
    self.setScale(2*radius, node)
    self.scale = max(self.scale)
    
  radius = property(getRadius, setRadius)
  
#-------------------------------------------------------------------------------

  def getGlobalRadius(self):
    return self.getRadius(render)
    
  def setGlobalRadius(self, radius):
    self.setRadius(radius, render)
    
  globalRadius = property(getGlobalRadius, setGlobalRadius)
  
#-------------------------------------------------------------------------------

  def fit(self, node):
    Geometry.fit(self, node)
    
    self.scale = max(self.scale)
    