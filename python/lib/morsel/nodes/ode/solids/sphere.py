from morsel.panda import *
from morsel.nodes.ode.solid import Solid
from morsel.nodes.ode.geometries.sphere import Sphere as Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Sphere(Solid):
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
    radius = 0.5*max(dx, dy, dz)

    geometry = Geometry(world, name+"Geometry", self, radius = radius)
    display = Mesh(name+"Display", "geometry/sphere.bam")
    
    Solid.__init__(self, world, name, mesh, geometry = geometry,
      display = display, position = [x, y, z], scale = 2*radius,
      parent = parent, **kargs)
