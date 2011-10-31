from morsel.core import *
from morsel.actors import Inanimate as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Inanimate(Base):
  def __init__(self, world, name, mesh, solid = None, body = None, mass = 0,
      **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.body.solid = Solid(name+"Solid", solid, self.body, body = body,
      mass = mass, parent = self.solid)
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.body.solid.body.body, self.solid.body.body)
    joint.set()
