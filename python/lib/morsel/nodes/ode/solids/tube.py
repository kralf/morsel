from morsel.panda import *
from morsel.nodes.ode.solid import Solid
from morsel.nodes.ode.geometries import Tube as Geometry
from morsel.nodes import Node
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Tube(Solid):
  def __init__(self, world, name, mesh, parent = None, **kargs):
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
      length = max(dz-2*radius, 0)
      orientation = [0, 0, 0]
    elif d_min == dxz:
      radius = 0.5*max(dx, dz)
      length = max(dy-2*radius, 0)
      orientation = [0, 90, 0]
    elif d_min == dyz:
      radius = 0.5*max(dy, dz)
      length = max(dx-2*radius, 0)
      orientation = [0, 0, 90]

    geometry = Geometry(world, name+"Geometry", self, radius = radius,
      length = length)
    display = Node(world, name+"Display")
    scale = [2*radius, 2*radius, length+2*radius]
    if length > 0:
      Mesh(name+"Display", "geometry/cylinder.bam",
        scale = [1, 1, length/scale[2]], parent = display)
    Mesh(name+"Display", "geometry/sphere.bam",
      position = [0, 0, -0.5*length/scale[2]],
      scale = [1, 1, 2*radius/scale[2]], parent = display)
    Mesh(name+"Display", "geometry/sphere.bam",
      position = [0, 0, 0.5*length/scale[2]],
      scale = [1, 1, 2*radius/scale[2]], parent = display)

    Solid.__init__(self, world, name, mesh, geometry = geometry,
      display = display, position = [x, y, z], orientation = orientation,
      scale = scale, parent = parent, **kargs)
