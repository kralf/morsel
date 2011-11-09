from morsel.panda import *
from morsel.nodes.ode.solid import Solid
from morsel.nodes.ode.geometries import Ray as Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Ray(Solid):
  def __init__(self, world, name, mesh = None, parent = None, **kargs):
    if mesh:
      p_min, p_max = mesh.getTightBounds()

      x = 0.5*(p_min[0]+p_max[0])
      y = 0.5*(p_min[1]+p_max[1])
      z = p_max[2]
      dz = abs(p_max[2]-p_min[2])
    else:
      x = 0
      y = 0
      z = 0
      dz = 0.6
    
    geometry = Geometry(world, name+"Geometry", self, start = [x, y, z],
      length = dz)
    display = Mesh(name+"Display", "geometry/cylinder.bam",
      position = [0, 0, 0.5*dz])

    Solid.__init__(self, world, name, mesh, geometry = geometry,
      display = display, position = [x, y, z-dz],
      scale = [0.01, 0.01, dz], parent = parent, **kargs)
