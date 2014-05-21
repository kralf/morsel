from morsel.nodes.platform import Platform as Base
from object import Object

#-------------------------------------------------------------------------------

class Platform(Object, Base):
  COLLISIONS_FROM = 0x000F0000
  COLLISIONS_INTO = 0xFFF0FF0F
  
  def __init__(self, collisionMasks = [COLLISIONS_FROM, COLLISIONS_INTO],
      **kargs):
    super(Platform, self).__init__(collisionMasks = collisionMasks, **kargs)
