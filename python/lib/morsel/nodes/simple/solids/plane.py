from morsel.core import *
from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Plane(Solid):
  def __init__(self, world, name, mesh, **kargs):
    p_min, p_max = mesh.getTightBounds()
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    dx = abs(p_max[0]-p_min[0])
    dy = abs(p_max[1]-p_min[1])
    dz = abs(p_max[2]-p_min[2])
    d_min = min(dx, dy, dz)

    if d_min == dx:
      normal = panda.Vec3(1, 0 , 0)
    elif d_min == dy:
      normal = panda.Vec3(0, 1 , 0)
    elif d_min == dz:
      normal = panda.Vec3(0, 0 , 1)

    plane = panda.Plane(normal, panda.Point3(x, y, z))
    geometry = panda.CollisionPlane(plane)

    Solid.__init__(self, world, name, mesh, geometry, **kargs)
