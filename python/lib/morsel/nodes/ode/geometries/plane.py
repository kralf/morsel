from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes import Node
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Plane(Geometry):
  def __init__(self, world, name, solid, scale = [1, 1, 1], **kargs):
    d_min = min(scale)

    if d_min == scale[0]:
      orientation = [0, 90, 0]
      scale = [1, 1e3*scale[1], 1e3*scale[2]]
    elif d_min == scale[1]:
      orientation = [0, 0, 90]
      scale = [1e3*scale[0], 1, 1e3*scale[2]]
    elif d_min == scale[2]:
      orientation = [0, 0, 0]
      scale = [1e3*scale[0], 1e3*scale[1], 1]
      
    geometry = panda.OdePlaneGeom(world.space, panda.Vec4(0, 0, 1, 0))
    
    Geometry.__init__(self, world, name, solid, geometry = geometry,
      orientation = orientation, scale = scale, **kargs)

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)
    self.setOrientation(self.orientation)
    
  position = property(Geometry.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)
    
    quaternion = panda.Quat()
    quaternion.setHpr(panda.Vec3(*orientation))
    normal = quaternion.xform(panda.Vec3(0, 0, 1))
    d = -normal.dot(self.getPos(self.world.scene))

    self.geometry.setParams(normal[0], normal[1], normal[2], d)

  orientation = property(Geometry.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(name = self.name+"Display", filename = "geometry/plane.bam")
  