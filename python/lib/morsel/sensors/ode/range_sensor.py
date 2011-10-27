from morsel.core import *
from morsel.sensors.range_sensor import RangeSensor as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class RangeSensor(Base):
  def __init__(self, world, name, mesh, solid = None, body = None, mass = 0,
      **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.solid = Solid(name+"Solid", solid, self.mesh, body = body,
      mass = mass, parent = self)
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.parent.solid.body.body, self.solid.body.body)
    joint.set()
