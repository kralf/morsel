from morsel.nodes import Actor
from morsel.actors.facade import Actuator

#-------------------------------------------------------------------------------

class Animate(Actor):
  def __init__(self, world, name, mesh, actuatorType = None, body = None,
      **kargs):
    actuator = Actuator(name+"Actuator", actuatorType, mesh, **kargs)

    Actor.__init__(self, world, name, actuator = actuator)

    self.mesh = mesh
    self.mesh.parent = self
    