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
    
    if not self.geometry:
      self.geometry = panda.CollisionRay()
      
    self.geometry.setOrigin(*self.origin)
    self.geometry.setDirection(*self.direction)
    