from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Plane(Geometry):
  def __init__(self, world, name, solid, **kargs):
    coefficients = panda.Vec4(0, 0, 1, 0)
    geometry = panda.OdePlaneGeom(world.space, coefficients)

    Geometry.__init__(self, world, name, solid, geometry = geometry, **kargs)

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
  