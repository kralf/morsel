from morsel.panda import *
from morsel.geometries.box import Box as Base
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Box(Solid, Base):
  def __init__(self, **kargs):
    super(Box, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    self.geometry = panda.OdeBoxGeom(node.world.space, *self.globalSize)
  