from morsel.panda import *
from morsel.nodes.static import Static as Base

#-------------------------------------------------------------------------------

class Static(Base):
  def __init__(self, world, name, mesh, solid = None, body = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    if not solid:
      solid = "Empty"
    if not body:
      body = "Empty"

    self.solid = Solid(name = name+"Solid", type = solid, mesh = self.mesh,
      body = body, parent = self.world.scene.solid)
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.solid.body.body, self.world.scene.solid.body.body)
    joint.set()
    