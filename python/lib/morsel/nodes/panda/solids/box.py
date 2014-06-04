from morsel.panda import *
from morsel.geometries.box import Box as Base
from morsel.nodes.panda.solid import Solid

#-------------------------------------------------------------------------------

class Box(Solid, Base):
  def __init__(self, **kargs):
    super(Box, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    self.geometry = panda.CollisionBox(panda.Point3(*self.minimum),
      panda.Point3(*self.maximum))

#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    if self.geometry:
      self.geometry = panda.CollisionBox(panda.Point3(*self.minimum),
        panda.Point3(*self.maximum))

#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self.geometry:
      self.geometry = panda.CollisionBox(panda.Point3(*self.minimum),
        panda.Point3(*self.maximum))
    