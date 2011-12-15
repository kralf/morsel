from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes import Node
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Tube(Geometry):
  def __init__(self, world, name, solid, scale = [1, 1, 1], **kargs):
    dxy = abs(scale[0]-scale[1])
    dxz = abs(scale[0]-scale[2])
    dyz = abs(scale[1]-scale[2])
    d_min = min(dxy, dxz, dyz)

    if d_min == dxy:
      radius = 0.5*max(scale[0], scale[1])
      length = max(scale[2]-2*radius, 0)
      orientation = [0, 0, 0]
    elif d_min == dxz:
      radius = 0.5*max(scale[0], scale[2])
      length = max(scale[1]-2*radius, 0)
      orientation = [0, 90, 0]
    elif d_min == dyz:
      radius = 0.5*max(scale[1], scale[2])
      length = max(scale[0]-2*radius, 0)
      orientation = [0, 0, 90]
    scale = [2*radius, 2*radius, length+2*radius]

    geometry = panda.OdeCappedCylinderGeom(world.space, radius, length)
    
    Geometry.__init__(self, world, name, solid, geometry = geometry,
      orientation = orientation, scale = scale, **kargs)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    display = Node(self.name+"Display")

    radius = self.geometry.getRadius()
    length = self.geometry.getLength()
    
    if length > 0:
      Mesh(name = self.name+"DisplayCylinder",
        filename = "geometry/cylinder.bam",
        scale = [1, 1, length/self.scale[2]], parent = display)
    Mesh(name = self.name+"DisplayCap", filename = "geometry/sphere.bam",
      position = [0, 0, -0.5*length/self.scale[2]],
      scale = [1, 1, 2*radius/self.scale[2]], parent = display)
    Mesh(name = self.name+"DisplayCap", filename = "geometry/sphere.bam",
      position = [0, 0, 0.5*length/self.scale[2]],
      scale = [1, 1, 2*radius/self.scale[2]], parent = display)

    return display
