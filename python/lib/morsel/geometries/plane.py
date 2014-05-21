from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Plane(Geometry):
  def __init__(self, normal = [0, 0, 1], size = [1, 1], **kargs):
    super(Plane, self).__init__(**kargs)
    
    self.normal = normal
    self.size = size

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:
      self._mesh = Mesh(filename = "geometry/plane.bam", parent = self)
      
    return self._mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def getNormal(self, node = None):
    if not node:
      node = self.parent
    
    normal = node.getRelativeVector(self, panda.Vec3(0, 0, 1))
    normal.normalize()
      
    return [normal[0], normal[1], normal[2]]
    
  def setNormal(self, normal, node = None):
    if not node:
      node = self.parent
      
    normal = self.parent.getRelativeVector(node, panda.Vec3(*normal))
    
    quaternion = Quaternion()
    quaternion.setFromVectors([0, 0, 1], normal)
    
    self.quaternion = quaternion
    
  normal = property(getNormal, setNormal)

#-------------------------------------------------------------------------------

  def getGlobalNormal(self):
    return self.getNormal(render)
    
  def setGlobalNormal(self, normal):
    self.setNormal(normal, render)
    
  globalNormal = property(getGlobalNormal, setGlobalNormal)

#-------------------------------------------------------------------------------

  def getSize(self, node = None):
    scale = self.getScale(node)
    return [scale[0], scale[1]]
    
  def setSize(self, size, node = None):
    scale = self.getScale(node)
    self.setScale([size[0], size[1], scale[2]], node)
    
  size = property(getSize, setSize)
  
#-------------------------------------------------------------------------------

  def getGlobalSize(self):
    return self.getSize(render)
    
  def setGlobalSize(self, size):
    self.setSize(size, render)
    
  globalSize = property(getGlobalSize, setGlobalSize)
  
#-------------------------------------------------------------------------------

  def fit(self, node):
    Geometry.fit(self, node)
    
    d_min = min(self.scale)

    if d_min == self.scale[0]:
      self.rotate([0, 90, 0])
      self.scale = [self.scale[2], self.scale[1], 1]
    elif d_min == self.scale[1]:
      self.rotate([0, 0, 90])
      self.scale = [self.scale[0], self.scale[2], 1]
    else:
      self.scale = [self.scale[0], self.scale[1], 1]
    