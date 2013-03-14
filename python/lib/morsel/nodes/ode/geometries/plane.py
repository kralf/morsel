from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes import Node
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Plane(Geometry):
  def __init__(self, world, name, solid, **kargs):
    Geometry.__init__(self, world, name, solid, placeable = False, **kargs)

    d_min = min(self.scale)

    if d_min == self.scale[0]:
      self.orientation = [0, 0, 90]
      self.scale = [1, 1e3*self.scale[1], 1e3*self.scale[2]]
    elif d_min == self.scale[1]:
      self.orientation = [0, 90, 0]
      self.scale = [1e3*self.scale[0], 1, 1e3*self.scale[2]]
    else:
      self.scale = [1e3*self.scale[0], 1e3*self.scale[1], 1]
    
    self.geometry = panda.OdePlaneGeom(world.space, panda.Vec4(0, 0, 1, 0))

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)
    self.setOrientation(self.orientation)
    
  position = property(Geometry.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)
    
    if self.geometry:
      quaternion = panda.Quat()
      quaternion.setHpr(panda.Vec3(*orientation))
      normal = quaternion.xform(panda.Vec3(0, 0, 1))
      d = -normal.dot(self.getPos(self.world.scene))

      self.geometry.setParams(normal[0], normal[1], normal[2], d)

  orientation = property(Geometry.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def setBody(self, body):
    self._body = body

  body = property(Geometry.getBody, setBody)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(name = self.name+"Display", filename = "geometry/plane.bam")
  