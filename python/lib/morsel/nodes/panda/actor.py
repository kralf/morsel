from morsel.nodes.actor import Actor as Base
from object import Object

#-------------------------------------------------------------------------------

class Actor(Object, Base):
  COLLISIONS_FROM = 0x0000F000
  COLLISIONS_INTO = 0xFFFFFF0F
  
  def __init__(self, collisionMasks = [COLLISIONS_FROM, COLLISIONS_INTO],
      **kargs):
    super(Actor, self).__init__(collisionMasks = collisionMasks, **kargs)
