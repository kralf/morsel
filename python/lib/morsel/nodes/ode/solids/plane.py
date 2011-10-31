from morsel.panda import *
from morsel.nodes.ode.solid import Solid
from morsel.nodes.ode.geometries.plane import Plane as Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Plane(Solid):
  def __init__(self, world, name, mesh, parent = None, **kargs):
    p_min, p_max = mesh.getTightBounds()
    p_min = parent.getRelativePoint(mesh.parent, p_min)
    p_max = parent.getRelativePoint(mesh.parent, p_max)
    
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    dx = abs(p_max[0]-p_min[0])
    dy = abs(p_max[1]-p_min[1])
    dz = abs(p_max[2]-p_min[2])
    d_min = min(dx, dy, dz)

    if d_min == dx:
      orientation = [0, 90, 0]
      scale = [1, 1e3*dy, 1e3*dz]
    elif d_min == dy:
      orientation = [0, 0, 90]
      scale = [1e3*dx, 1, 1e3*dz]
    elif d_min == dz:
      orientation = [0, 0, 0]
      scale = [1e3*dx, 1e3*dy, 1]
      
    geometry = Geometry(world, name+"Geometry", self)
    display = Mesh(name+"Display", "geometry/plane.bam")

    Solid.__init__(self, world, name, mesh, geometry = geometry,
      display = display, position = [x, y, z], orientation = orientation,
      scale = scale, parent = parent, **kargs)
  