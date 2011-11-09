from morsel.panda import *
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
      radius = 0.5*max(dx, dy)
      a = panda.Point3(x, y, min(z, p_min[2]+radius))
      b = panda.Point3(x, y, max(z, p_max[2]-radius))
    elif d_min == dxz:
      radius = 0.5*max(dx, dz)
      a = panda.Point3(x, min(y, p_min[1]+radius), z)
      b = panda.Point3(x, max(y, p_max[1]-radius), z)
    elif d_min == dyz:
      radius = 0.5*max(dy, dz)
      a = panda.Point3(min(x, p_min[0]+radius), y, z)
      b = panda.Point3(max(x, p_max[0]-radius), y, z)
      
    geometry = panda.CollisionTube(a, b, radius)
    
    Solid.__init__(self, world, name, mesh, geometry, **kargs)
