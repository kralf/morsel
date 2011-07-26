from morsel.core import *
from morsel.nodes.ode.solid import Solid
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Box(Solid):
  def __init__(self, world, name, mesh, body = None, mass = 0, parent = None,
      **kargs):
    p_min, p_max = mesh.getTightBounds()
    p_min = parent.getRelativeVector(mesh, p_min)
    p_max = parent.getRelativeVector(mesh, p_max)
    
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    dx = abs(p_max[0]-p_min[0])
    dy = abs(p_max[1]-p_min[1])
    dz = abs(p_max[2]-p_min[2])
    
    geometry = panda.OdeBoxGeom(world.space, dx, dy, dz)
    display = Mesh(name+"Display", "geometry/cube.bam", scale = [dx, dy, dz])

    Solid.__init__(self, world, name, mesh, geometry = geometry,
      body = body, mass = mass, display = display, position = [x, y, z],
      parent = parent, **kargs)
    