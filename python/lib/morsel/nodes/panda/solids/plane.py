from morsel.panda import *
from morsel.geometries.plane import Plane as Base
from morsel.nodes.panda.solid import Solid

#-------------------------------------------------------------------------------

class Plane(Solid, Base):
  def __init__(self, **kargs):
    super(Plane, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    plane = panda.Plane(panda.Vec3(*self.normal), panda.Point3(
      *self.position))
    
    if not self.geometry:
      self.geometry = panda.CollisionPlane(plane)
    else:
      self.geometry.setPlane(plane)
  