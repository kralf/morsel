from morsel.nodes import Actor
from morsel.actors.facade import Actuator
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Character(Actor):
  def __init__(self, world, name, mesh, actuatorType = None, body = None,
      bodyAnimation = None, **kargs):
    self.motor = Actuator(name = name+"Motor", type = actuatorType,
      mesh = mesh, **kargs)
    self.body = None

    Actor.__init__(self, world, name, actuator = self.motor)

    if body:
      bodyModel = mesh.find("**/"+body)
      if not bodyModel.isEmpty():
        self.body = Mesh(name = name+"Body", model = bodyModel,
          animation = bodyAnimation, parent = self)
      else:
        framework.error("Body model '"+body+"' not found")
      