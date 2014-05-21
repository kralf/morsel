from morsel.panda import *
from morsel.nodes.facade import Mesh
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Ray(Geometry):
  def __init__(self, length = 1, **kargs):
    super(Ray, self).__init__(**kargs)
    
    self.length = length

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:
      geometryData = panda.GeomVertexData("VertexData",
        panda.GeomVertexFormat.getV3(), panda.Geom.UHDynamic)
      linestrip = panda.GeomLinestrips(panda.Geom.UHStatic)
      geometry = panda.Geom(geometryData)
      geometry.addPrimitive(linestrip)
      geometryNode = panda.GeomNode("Geometry")
      geometryNode.addGeom(geometry)
      
      self._mesh = Node(name = "Mesh", parent = self)      
      self._mesh.attachNewNode(geometryNode)
      
      writer = panda.GeomVertexWriter(geometryData, "vertex")
      writer.addData3f(0, 0, 0)
      writer.addData3f(0, 0, -1)
      linestrip.addVertices(0, 1)
      linestrip.closePrimitive()

    return self._mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def getLength(self, node = None):
    return self.getScale(node)[2]
  
  def setLength(self, length, node = None):
    scale = self.getScale(node)
    self.setScale([scale[0], scale[1], length], node)
  
  length = property(getLength, setLength)

#-------------------------------------------------------------------------------

  def getGlobalLength(self):
    return self.getLength(render)
  
  def setGlobalLength(self, length):
    self.setLength(length, render)
  
  globalLength = property(getGlobalLength, setGlobalLength)

#-------------------------------------------------------------------------------

  def getOrigin(self, node = None):
    if not node:
      node = self.parent
      
    origin = node.getRelativePoint(self, panda.Point3(0, 0, 0))
    
    return [origin[0], origin[1], origin[2]]
  
  origin = property(getOrigin)

#-------------------------------------------------------------------------------

  def getGlobalOrigin(self):
    return self.getOrigin(render)
  
  globalOrigin = property(getGlobalOrigin)

#-------------------------------------------------------------------------------

  def getDirection(self, node = None):
    if not node:
      node = self.parent
      
    direction = node.getRelativeVector(self, panda.Vec3(0, 0, -1))
    direction.normalize()
    
    return [direction[0], direction[1], direction[2]]
  
  direction = property(getDirection)

#-------------------------------------------------------------------------------

  def getGlobalDirection(self):
    return self.getDirection(render)
  
  globalDirection = property(getGlobalDirection)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Geometry.fit(self, node)
    
    d_xy = abs(self.scale[0]-self.scale[1])
    d_xz = abs(self.scale[0]-self.scale[2])
    d_yz = abs(self.scale[1]-self.scale[2])
    d_min = min(d_xy, d_xz, d_yz)

    if d_min == d_xz:
      self.y += 0.5*self.scale[1]
      self.rotate([0, 0, 90])
      self.scale = [0, 0, self.scale[1]]
    elif d_min == d_yz:
      self.x += 0.5*self.scale[0]
      self.rotate([0, 90, 0])
      self.scale = [0, 0, self.scale[0]]
    else:
      self.z += 0.5*self.scale[2]
      self.scale = [0, 0, self.scale[2]]
    