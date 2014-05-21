from morsel.panda import *
from morsel.geometries.cylinder import Cylinder as Base
from morsel.nodes.ode.body import Body

#-------------------------------------------------------------------------------

class Cylinder(Body, Base):
  def __init__(self, **kargs):
    super(Cylinder, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    super(Cylinder, self).fit(node)
    
    mass = panda.OdeMass()
    mass.setCylinderTotal(self.mass, 3, self.globalRadius, self.globalHeight)
    
    self._body.setMass(mass)
  