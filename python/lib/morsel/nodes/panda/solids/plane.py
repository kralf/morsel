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
    self.geometry = panda.CollisionPlane(plane)
    
#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    if self.geometry:
      plane = panda.Plane(panda.Vec3(*self.normal), panda.Point3(
        *self.position))
      self.geometry.setPlane(plane)
    
#-------------------------------------------------------------------------------

  def onRotate(self, rotation):
    if self.geometry:
      plane = panda.Plane(panda.Vec3(*self.normal), panda.Point3(
        *self.position))
      self.geometry.setPlane(plane)
  