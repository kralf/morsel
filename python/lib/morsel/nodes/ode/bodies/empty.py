from morsel.panda import *
from morsel.nodes.ode.body import Body

#-------------------------------------------------------------------------------

class Empty(Body):
  def __init__(self, world, name, solid, mass = 0, scale = [1, 1, 1],
      **kargs):
    Body.__init__(self, world, name, solid, **kargs)
