from morsel.panda import *
from morsel.geometries.plane import Plane as Base
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Plane(Solid, Base):
  def __init__(self, **kargs):
    super(Plane, self).__init__(placeable = False, **kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    normal = self.globalNormal
    self.geometry = panda.OdePlaneGeom(node.world.space,
      panda.Vec4(normal[0], normal[1], normal[2], 0))

#-------------------------------------------------------------------------------

  def onRotate(self, rotation):
    if self.geometry:
      normal = self.globalNormal
      self.geometry.setParams(normal[0], normal[1], normal[2], 0)
      