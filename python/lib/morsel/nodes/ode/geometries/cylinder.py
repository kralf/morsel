from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Cylinder(Geometry):
  def __init__(self, world, name, solid, **kargs):
    Geometry.__init__(self, world, name, solid, **kargs)

    dxy = abs(self.globalScale[0]-self.globalScale[1])
    dxz = abs(self.globalScale[0]-self.globalScale[2])
    dyz = abs(self.globalScale[1]-self.globalScale[2])
    d_min = min(dxy, dxz, dyz)

    if d_min == dxy:
      radius = 0.5*max(self.globalScale[0], self.globalScale[1])
      length = self.globalScale[2]
    elif d_min == dxz:
      radius = 0.5*max(self.globalScale[0], self.globalScale[2])
      length = self.globalScale[1]
      self.orientation = [0, 0, 90]
      self.scale = [self.scale[0], self.scale[2], self.scale[1]]
    else:
      radius = 0.5*max(self.globalScale[1], self.globalScale[2])
      length = self.globalScale[0]
      self.orientation = [0, 90, 0]
      self.scale = [self.scale[2], self.scale[1], self.scale[0]]

    self.geometry = panda.OdeCylinderGeom(world.space, radius, length)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return Mesh(name = self.name+"Display", filename = "geometry/cylinder.bam")
