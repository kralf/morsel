from morsel.panda import *
from morsel.geometries.sphere import Sphere as Base
from morsel.nodes.panda.solid import Solid

#-------------------------------------------------------------------------------

class Sphere(Solid, Base):
  def __init__(self, **kargs):    
    super(Sphere, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    self.geometry = panda.CollisionSphere(panda.Point3(*self.position),
      self.radius)
    
#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    if self.geometry:
      self.geometry.setCenter(*self.position)
  
#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self.geometry:
      self.geometry.setRadius(self.radius)
      