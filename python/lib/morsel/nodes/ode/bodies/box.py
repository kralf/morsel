from morsel.panda import *
from morsel.nodes.ode.body import Body
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Box(Body):
  def __init__(self, world, name, solid, mass = 0, **kargs):
    p_min, p_max = solid.mesh.getTightBounds()
    
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    dx = abs(p_max[0]-p_min[0])
    dy = abs(p_max[1]-p_min[1])
    dz = abs(p_max[2]-p_min[2])

    _mass = panda.OdeMass()
    _mass.setBoxTotal(mass, dx, dy, dz)

    Body.__init__(self, world, name, solid, mass = _mass, position = [x, y, z],
      **kargs)
