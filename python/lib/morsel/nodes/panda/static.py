from facade import Solid
from morsel.nodes.static import Static as Base
from object import Object

#-------------------------------------------------------------------------------

class Static(Object, Base):
  COLLISIONS_FROM = 0x0000000F
  COLLISIONS_INTO = 0xFFFFFFF0
  
  def __init__(self, solid = None, collisionMasks = [COLLISIONS_FROM,
      COLLISIONS_INTO], **kargs):
    super(Static, self).__init__(collisionMasks = collisionMasks, **kargs)

    self.solid = Solid(type = solid)
      