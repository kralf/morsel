from morsel.panda import *
from morsel.geometries.sphere import Sphere as Base
from morsel.nodes.ode.body import Body

#-------------------------------------------------------------------------------

class Sphere(Body, Base):
  def __init__(self, **kargs):
    super(Sphere, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    super(Sphere, self).fit(node)
    
    mass = panda.OdeMass()
    mass.setSphereTotal(self.mass, self.globalRadius)
    
    self._body.setMass(mass)
