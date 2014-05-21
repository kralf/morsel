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
    
    if not self.geometry:
      self.geometry = panda.CollisionSphere(self.position[0],
        self.position[1], self.position[2], self.radius)
    else:
      self.geometry.setCenter(*self.position)
      self.geometry.setRadius(self.radius)
      