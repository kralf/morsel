from morsel.panda import *
from morsel.nodes.ode.body import Body

#-------------------------------------------------------------------------------

class Box(Body):
  def __init__(self, world, name, solid, mass = 0, scale = [1, 1, 1],
      **kargs):
    box = panda.OdeMass()
    box.setBoxTotal(mass, *scale)
    
    Body.__init__(self, world, name, solid, mass = box, scale = scale,
      **kargs)
    