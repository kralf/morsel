from morsel.panda import *
from morsel.nodes.facade import Mesh
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Tube(Geometry):
  def __init__(self, radius = 0.5, height = 1, **kargs):
    super(Tube, self).__init__(**kargs)
    
    self.radius = radius
    self.height = height

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:      
      self._mesh = Mesh(filename = "geometry/tube.bam", parent = self)
      
      self._meshCylinder = self._mesh.find("**/Cylinder")
      self._meshLowerCap = self._mesh.find("**/LowerCap")
      self._meshUpperCap = self._mesh.find("**/UpperCap")

      self.onScale([1, 1, 1])
      
    return self._mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def getRadius(self, node = None):    
    scale = self.getScale(node)
    return 0.5*max(scale[0], scale[1])
    
  def setRadius(self, radius, node = None):
    scale = self.getScale(node)
    height = max(scale[2]-2*radius, 0)
    
    self.setScale([2*radius, 2*radius, height+2*radius], node)
    
  radius = property(getRadius, setRadius)
  
#-------------------------------------------------------------------------------

  def getGlobalRadius(self):
    return self.getRadius(render)
    
  def setGlobalRadius(self, radius):
    self.setRadius(radius, render)
    
  globalRadius = property(getGlobalRadius, setGlobalRadius)
  
#-------------------------------------------------------------------------------

  def getHeight(self, node = None):
    scale = self.getScale(node)
    radius = 0.5*max(scale[0], scale[1])
    
    return max(scale[2]-2*radius, 0)
  
  def setHeight(self, height, node = None):
    scale = self.getScale(node)
    radius = 0.5*max(scale[0], scale[1])
    
    self.setScale([scale[0], scale[1], height+2*radius], node)
  
  height = property(getHeight, setHeight)

#-------------------------------------------------------------------------------

  def getGlobalHeight(self):
    return self.getHeight(render)
    
  def setGlobalHeight(self, radius):
    self.setHeight(height, render)
    
  globalHeight = property(getGlobalHeight, setGlobalHeight)
  
#-------------------------------------------------------------------------------

  def getA(self, node = None):
    if not node:
      node = self.parent
      
    a = node.getRelativePoint(self, panda.Point3(0, 0, -0.5*self.height))
    
    return [a[0], a[1], a[2]]
    
  a = property(getA)

#-------------------------------------------------------------------------------

  def getGlobalA(self):
    return self.getA(render)
    
  globalA = property(getGlobalA)

#-------------------------------------------------------------------------------

  def getB(self, node = None):
    if not node:
      node = self.parent
      
    b = node.getRelativePoint(self, panda.Point3(0, 0, 0.5*self.height))
    
    return [b[0], b[1], b[2]]
    
  b = property(getB)

#-------------------------------------------------------------------------------

  def getGlobalB(self):
    return self.getB(render)
    
  globalB = property(getGlobalB)

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
    height = max(self.scale[2]-2*radius, 0)
    
    self.scale = [2*radius, 2*radius, height+2*radius]

#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self._mesh:
      scale = self.scale
      radius = 0.5*max(scale[0], scale[1])
      height = max(scale[2]-2*radius, 0)/(2*radius)
      
      self._mesh.setScale([2*radius/scale[0], 2*radius/scale[1],
        2*radius/scale[2]])
      
      if height > 0:
        self._meshCylinder.setSz(height)
        self._meshCylinder.unstash()
      else:
        self._meshCylinder.stash()
        
      self._meshLowerCap.setZ(-0.5*height)
      self._meshUpperCap.setZ(0.5*height)
      