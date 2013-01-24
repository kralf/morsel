from morsel.panda import *
from morsel.nodes.simple.geometry import Geometry

#-------------------------------------------------------------------------------

class Plane(Geometry):
  def __init__(self, world, name, solid, scale = [1, 1, 1], **kargs):
    d_min = min(scale)

    if d_min == scale[0]:
      normal = panda.Vec3(1, 0 , 0)
    elif d_min == scale[1]:
      normal = panda.Vec3(0, 1 , 0)
    elif d_min == scale[2]:
      normal = panda.Vec3(0, 0 , 1)

    plane = panda.Plane(normal, panda.Point3(0, 0, 0))
    geometry = panda.CollisionPlane(plane)

    Geometry.__init__(self, world, name, solid, geometry = geometry,
      scale = scale, **kargs)
