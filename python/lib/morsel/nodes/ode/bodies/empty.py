from morsel.core import *
from morsel.nodes.ode.body import Body

#-------------------------------------------------------------------------------

class Empty(Body):
  def __init__(self, world, name, solid = None, **kargs):
    Body.__init__(self, world, name, solid, **kargs)
