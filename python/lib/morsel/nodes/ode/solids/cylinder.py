from morsel.core import *
from morsel.nodes.ode.solid import Solid
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Cylinder(Solid):
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
    dxy = abs(dx-dy)
    dxz = abs(dx-dz)
    dyz = abs(dy-dz)
    d_min = min(dxy, dxz, dyz)

    if d_min == dxy:
      radius = 0.5*max(dx, dy)
      length = dz
      orientation = [0, 0, 0]
    elif d_min == dxz:
      radius = 0.5*max(dx, dz)
      length = dy
      orientation = [0, 90, 0]
    elif d_min == dyz:
      radius = 0.5*max(dy, dz)
      length = dx
      orientation = [0, 0, 90]

    geometry = panda.OdeCylinderGeom(world.space, radius, length)
    display = Mesh(name+"Display", "geometry/cylinder.bam",
      scale = [2*radius, 2*radius, length])

    Solid.__init__(self, world, name, mesh, geometry = geometry,
      body = body, mass = mass, display = display, position = [x, y, z],
      orientation = orientation, parent = parent, **kargs)
