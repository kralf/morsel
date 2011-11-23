from morsel.panda import *
from morsel.nodes.simple.geometry import Geometry

#-------------------------------------------------------------------------------

class Tube(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      scale = [1, 1, 1], **kargs):
    p_min = panda.Vec3(*position)-panda.Vec3(*scale)*0.5
    p_max = panda.Vec3(*position)+panda.Vec3(*scale)*0.5
    dxy = abs(scale[0]-scale[1])
    dxz = abs(scale[0]-scale[2])
    dyz = abs(scale[1]-scale[2])
    d_min = min(dxy, dxz, dyz)

    if d_min == dxy:
      radius = 0.5*max(scale[0], scale[1])
      a = panda.Point3(position[0], position[1],
        min(position[2], p_min[2]+radius))
      b = panda.Point3(position[0], position[1],
        max(position[2], p_max[2]-radius))
    elif d_min == dxz:
      radius = 0.5*max(scale[0], scale[2])
      a = panda.Point3(position[0], min(position[1], p_min[1]+radius),
        position[2])
      b = panda.Point3(position[0], max(position[1], p_max[1]-radius),
        position[2])
    elif d_min == dyz:
      radius = 0.5*max(scale[1], scale[2])
      a = panda.Point3(min(position[0], p_min[0]+radius), position[1],
        position[2])
      b = panda.Point3(max(position[0], p_max[0]-radius), position[1],
        position[2])
      
    geometry = panda.CollisionTube(a, b, radius)
    
    Geometry.__init__(self, world, name, solid, geometry, position = position,
      scale = scale, **kargs)
