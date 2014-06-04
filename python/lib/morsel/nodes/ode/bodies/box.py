from morsel.panda import *
from morsel.geometries.box import Box as Base
from morsel.nodes.ode.body import Body

#-------------------------------------------------------------------------------

class Box(Body, Base):
  def __init__(self, **kargs):
    super(Box, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    super(Box, self).fit(node)
    
    mass = panda.OdeMass()
    mass.setBoxTotal(self.mass, *self.globalSize)
    
    self._body.setMass(mass)

#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self._body:
      mass = panda.OdeMass()
      mass.setBoxTotal(self.mass, *self.globalSize)
      
      self._body.setMass(mass)
    