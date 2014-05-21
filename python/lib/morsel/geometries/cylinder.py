from morsel.panda import *
from morsel.nodes.facade import Mesh
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Cylinder(Geometry):
  def __init__(self, radius = 0.5, height = 1, **kargs):
    super(Cylinder, self).__init__(**kargs)
    
    self.radius = radius
    self.height = height

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:
      self._mesh = Mesh(filename = "geometry/cylinder.bam", parent = self)
      
    return self._mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def getRadius(self, node = None):    
    scale = self.getScale(node)    
    return 0.5*max(scale[0], scale[1])
    
  def setRadius(self, radius, node = None):
    scale = self.getScale(node)
    self.setScale([2*radius, 2*radius, scale[2]], node)
    
  radius = property(getRadius, setRadius)
  
#-------------------------------------------------------------------------------

  def getGlobalRadius(self):
    return self.getRadius(render)
    
  def setGlobalRadius(self, radius):
    self.setRadius(radius, render)
    
  globalRadius = property(getGlobalRadius, setGlobalRadius)
  
#-------------------------------------------------------------------------------

  def getHeight(self, node = None):
    return self.getScale(node)[2]
  
  def setHeight(self, height, node = None):
    scale = self.getScale(node)
    self.setScale([scale[0], scale[1], height], node)
  
  height = property(getHeight, setHeight)

#-------------------------------------------------------------------------------

  def getGlobalHeight(self):
    return self.getHeight(render)
    
  def setGlobalHeight(self, radius):
    self.setHeight(height, render)
    
  globalHeight = property(getGlobalHeight, setGlobalHeight)
  
#-------------------------------------------------------------------------------

  def fit(self, node):
    Geometry.fit(self, node)
    
    d_xy = abs(self.scale[0]-self.scale[1])
    d_xz = abs(self.scale[0]-self.scale[2])
    d_yz = abs(self.scale[1]-self.scale[2])
    d_min = min(d_xy, d_xz, d_yz)

    if d_min == d_xz:
      self.rotate([0, 0, 90])
      self.scale = [self.scale[0], self.scale[2], self.scale[1]]
    elif d_min == d_yz:
      self.rotate([0, 90, 0])
      self.scale = [self.scale[2], self.scale[1], self.scale[0]]

    radius = 0.5*max(self.scale[0], self.scale[1])
    self.scale = [2*radius, 2*radius, self.scale[2]]
    