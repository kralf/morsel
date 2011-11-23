from morsel.panda import *
from morsel.nodes.simple.geometry import Geometry

#-------------------------------------------------------------------------------

class Box(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      scale = [1, 1, 1], **kargs):
    p_min = panda.Vec3(*position)-panda.Vec3(*scale)*0.5
    p_max = panda.Vec3(*position)+panda.Vec3(*scale)*0.5
    
    geometry = panda.CollisionBox(panda.Point3(p_min), panda.Point3(p_max))

    Geometry.__init__(self, world, name, solid, geometry = geometry,
      position = position, scale = scale, **kargs)
