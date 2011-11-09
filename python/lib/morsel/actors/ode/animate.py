from morsel.panda import *
from morsel.actors import Animate as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Animate(Base):
  def __init__(self, world, name, mesh, solid = None, body = None, mass = 0,
      massOffset = [0, 0, 0], **kargs):
    mesh = Mesh(name+"Mesh", mesh)
    Base.__init__(self, world, name, mesh, **kargs)

    self.mesh.solid = Solid(name+"Solid", solid, self.mesh, body = body,
      mass = mass, massOffset = massOffset, parent = self.solid)
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.mesh.solid.body.body, self.solid.body.body)
    joint.set()
    