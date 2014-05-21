from morsel.nodes.sensor import Sensor as Base
from object import Object

#-------------------------------------------------------------------------------

class Sensor(Object, Base):
  COLLISIONS_FROM = 0x00000F00
  COLLISIONS_INTO = 0xFFF000FF
  
  def __init__(self, collisionMasks = [COLLISIONS_FROM, COLLISIONS_INTO],
      **kargs):
    super(Sensor, self).__init__(collisionMasks = collisionMasks, **kargs)
