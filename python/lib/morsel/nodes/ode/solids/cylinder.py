from morsel.panda import *
from morsel.geometries.cylinder import Cylinder as Base
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Cylinder(Solid, Base):
  def __init__(self, **kargs):
    super(Cylinder, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)
    
    self.geometry = panda.OdeCylinderGeom(node.world.space,
      self.globalRadius, self.globalHeight)
