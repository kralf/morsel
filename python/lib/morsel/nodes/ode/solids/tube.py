from morsel.panda import *
from morsel.geometries.tube import Tube as Base
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Tube(Solid, Base):
  def __init__(self, **kargs):
    super(Tube, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)

    self.geometry = panda.OdeCappedCylinderGeom(node.world.space,
      self.globalRadius, self.globalHeight)

#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    if self.geometry:
      self.geometry.setParams(self.globalRadius, self.globalHeight)
      