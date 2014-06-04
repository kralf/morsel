from morsel.panda import *
from morsel.geometries.sphere import Sphere as Base
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Sphere(Solid, Base):
  def __init__(self, **kargs):
    super(Sphere, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    self.geometry = panda.OdeSphereGeom(node.world.space, self.globalRadius)

#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self.geometry:
      self.geometry.setRadius(self.globalRadius)
    