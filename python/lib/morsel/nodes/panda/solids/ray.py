from morsel.panda import *
from morsel.geometries.ray import Ray as Base
from morsel.nodes.panda.solid import Solid

#-------------------------------------------------------------------------------

class Ray(Solid, Base):
  def __init__(self, **kargs):
    super(Ray, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    self.geometry = panda.CollisionRay(panda.Point3(*self.origin),
      panda.Vec3(*self.direction))
    
#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    if self.geometry:
      self.geometry.setOrigin(*self.origin)
    
#-------------------------------------------------------------------------------

  def onRotate(self, rotation):
    if self.geometry:
      self.geometry.setDirection(*self.direction)
    