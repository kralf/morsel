from morsel.core import *
from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Plane(Solid):
  def __init__(self, world, name, mesh, normal = [0, 0, 1], **kargs):
    p_min, p_max = mesh.getTightBounds()
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])    

    plane = panda.Plane(panda.Vec3(*normal), panda.Point3(x, y, z))
    geometry = panda.CollisionPlane(plane)

    Solid.__init__(self, world, name, mesh, geometry, **kargs)
