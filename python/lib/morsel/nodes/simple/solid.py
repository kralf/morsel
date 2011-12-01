from morsel.nodes.solid import Solid as Base
from morsel.nodes.simple.facade import Geometry

#-------------------------------------------------------------------------------

class Solid(Base):
  def __init__(self, world, name, mesh = None, geometry = None, parent = None,
      **kargs):
    self.geometry = None

    Base.__init__(self, world, name, mesh = mesh, parent = parent, **kargs)

    if mesh:
      p_min, p_max = mesh.getBounds(self)
      x = 0.5*(p_min[0]+p_max[0])
      y = 0.5*(p_min[1]+p_max[1])
      z = 0.5*(p_min[2]+p_max[2])
      dx = abs(p_max[0]-p_min[0])
      dy = abs(p_max[1]-p_min[1])
      dz = abs(p_max[2]-p_min[2])

      position = [x, y, z]
      scale = [dx, dy, dz]
    else:
      position = [0, 0, 0]
      scale = [0, 0, 0]

    if geometry:
      self.geometry = Geometry(name = name+"Geometry", type = geometry,
        solid = self, position = position, scale = scale, parent = self)
      parent.collider.addSolid(self)
