from morsel.nodes import Actor
from morsel.actors.facade import Actuator
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Character(Actor):
  def __init__(self, world, name, mesh, actuatorType = None, body = None,
      **kargs):
    self.motor = Actuator(name+"Motor", actuatorType, mesh, **kargs)
    self.body = None

    Actor.__init__(self, world, name, actuator = self.motor)

    if body:
      bodyModel = mesh.find("**/"+body)
      if not bodyModel.isEmpty():
        self.body = Mesh(name+"Body", model = bodyModel, parent = self)
      else:
        framework.error("Body model '"+body+"' not found")
      