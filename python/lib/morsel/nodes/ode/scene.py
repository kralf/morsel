from morsel.panda import *
from morsel.nodes import Scene as Base

#-------------------------------------------------------------------------------

class Scene(Base):
  def __init__(self, world, name, **kargs):
    Base.__init__(self, world, name, **kargs)

    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.solid.body.body, None)
    joint.set()
