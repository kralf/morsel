from morsel.geometries.empty import Empty as Base
from morsel.nodes.ode.body import Body

#-------------------------------------------------------------------------------

class Empty(Body, Base):
  def __init__(self, mass = 1e-3, **kargs):
    super(Empty, self).__init__(mass = mass, **kargs)
    