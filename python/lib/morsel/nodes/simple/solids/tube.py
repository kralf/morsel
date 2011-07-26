from morsel.core import *
from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Tube(Solid):
  def __init__(self, world, name, mesh, **kargs):
    p_min, p_max = mesh.getTightBounds()
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    dx = abs(p_max[0]-p_min[0])
    dy = abs(p_max[1]-p_min[1])
    dz = abs(p_max[2]-p_min[2])
    dxy = abs(dx-dy)
    dxz = abs(dx-dz)
    dyz = abs(dy-dz)
    d_min = min(dxy, dxz, dyz)

    if d_min == dxy:
      a = panda.Point3(x, y, p_min[2])
      b = panda.Point3(x, y, p_max[2])
      radius = 0.5*max(dx, dy)
    elif d_min == dxz:
      a = panda.Point3(x, p_min[1], z)
      b = panda.Point3(x, p_max[1], z)
      radius = 0.5*max(dx, dz)
    elif d_min == dyz:
      a = panda.Point3(p_min[0], y, z)
      b = panda.Point3(p_max[0], y, z)
      radius = 0.5*max(dy, dz)
      
    geometry = panda.CollisionTube(a, b, radius)
    
    Solid.__init__(self, world, name, mesh, geometry, **kargs)
