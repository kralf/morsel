from morsel.geometries.empty import Empty as Base
from morsel.nodes.panda.solid import Solid

#-------------------------------------------------------------------------------

class Empty(Solid, Base):
  def __init__(self, **kargs):
    super(Empty, self).__init__(**kargs)
    