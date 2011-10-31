from morsel.panda import *
from morsel.platforms import Wheeled as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Wheeled(Base):
  def __init__(self, world, name, mesh, bodySolid = None, bodyBody = None,
      bodyMass = 0, bodyMassOffset = [0, 0, 0], **kargs):
    mesh = Mesh(name+"Mesh", mesh)
    Base.__init__(self, world, name, mesh, bodyMass = bodyMass, **kargs)

    self.body.solid = Solid(name+"BodySolid", bodySolid, self,
      body = bodyBody, mass = bodyMass, massOffset = bodyMassOffset,
      parent = self.chassis.solid)
      
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.chassis.solid.body.body, self.body.solid.body.body)
    joint.set()
