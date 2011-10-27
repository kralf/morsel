from morsel.core import *
from morsel.nodes.ode.body import Body
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Sphere(Body):
  def __init__(self, world, name, solid, mass = 0, **kargs):
    p_min, p_max = solid.mesh.getTightBounds()
    p_min = solid.getRelativePoint(solid.mesh.parent, p_min)
    p_max = solid.getRelativePoint(solid.mesh.parent, p_max)
    
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    dx = abs(p_max[0]-p_min[0])
    dy = abs(p_max[1]-p_min[1])
    dz = abs(p_max[2]-p_min[2])
    radius = 0.5*max(dx, dy, dz)

    _mass = panda.OdeMass()
    _mass.setSphereTotal(mass, radius)

    Body.__init__(self, world, name, solid, mass = _mass, position = [x, y, z],
      **kargs)
