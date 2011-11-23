from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Cylinder(Geometry):
  def __init__(self, world, name, solid, scale = [1, 1, 1], **kargs):
    dxy = abs(scale[0]-scale[1])
    dxz = abs(scale[0]-scale[2])
    dyz = abs(scale[1]-scale[2])
    d_min = min(dxy, dxz, dyz)

    if d_min == dxy:
      radius = 0.5*max(scale[0], scale[1])
      length = scale[2]
      orientation = [0, 0, 0]
    elif d_min == dxz:
      radius = 0.5*max(scale[0], scale[2])
      length = scale[1]
      orientation = [0, 90, 0]
      scale = [scale[0], scale[2], scale[1]]
    elif d_min == dyz:
      radius = 0.5*max(scale[1], scale[2])
      length = scale[0]
      orientation = [0, 0, 90]
      scale = [scale[2], scale[1], scale[0]]

    geometry = panda.OdeCylinderGeom(world.space, radius, length)

    Geometry.__init__(self, world, name, solid, geometry = geometry,
      orientation = orientation, scale = scale, **kargs)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(self.name+"Display", "geometry/cylinder.bam")
