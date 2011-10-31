from morsel.panda import *
from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Sphere(Solid):
  def __init__(self, world, name, mesh, **kargs):
    p_min, p_max = mesh.getTightBounds()
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    radius = 0.5*max(abs(p_max[0]-p_min[0]), abs(p_max[1]-p_min[1]),
      abs(p_max[2]-p_min[2]))
      
    geometry = panda.CollisionSphere(x, y, z, radius)

    Solid.__init__(self, world, name, mesh, geometry, **kargs)
