from globals import *
from actuated import Actuated

#-------------------------------------------------------------------------------

class Actor(Actuated):
  def __init__(self, world, name, collisionMasks = [ACTOR_COLLISIONS_FROM,
      ACTOR_COLLISIONS_INTO], **kargs):
    Actuated.__init__(self, world, name, collisionMasks = collisionMasks,
      **kargs)
