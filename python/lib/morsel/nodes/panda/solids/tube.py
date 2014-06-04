from morsel.panda import *
from morsel.geometries.tube import Tube as Base
from morsel.nodes.panda.solid import Solid

#-------------------------------------------------------------------------------

class Tube(Solid, Base):
  def __init__(self, **kargs):
    super(Tube, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    self.geometry = panda.CollisionTube(panda.Point3(*self.a),
      panda.Point3(*self.b), self.radius)
    
#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    if self.geometry:
      self.geometry.setPointA(panda.Point3(*self.a))
      self.geometry.setPointB(panda.Point3(*self.b))
      self.geometry.setRadius(self.radius)
    
#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self.geometry:
      self.geometry.setPointA(panda.Point3(*self.a))
      self.geometry.setPointB(panda.Point3(*self.b))
      self.geometry.setRadius(self.radius)
  