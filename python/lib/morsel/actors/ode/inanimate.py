from morsel.panda import *
from morsel.actors import Inanimate as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Inanimate(Base):
  def __init__(self, world, name, mesh, solid = None, body = None, mass = 0,
      **kargs):
    mesh = Mesh(name+"Mesh", mesh)
    Base.__init__(self, world, name, mesh, **kargs)

    self.mesh.solid = Solid(name+"MeshSolid", solid, self.mesh, body = body,
      mass = mass, parent = self.solid)
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.solid.body.body, self.mesh.solid.body.body)
    joint.set()
