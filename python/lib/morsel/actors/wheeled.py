from morsel.nodes import Actor
from morsel.nodes.facade import Mesh
from morsel.actors.facade import Actuator

#-------------------------------------------------------------------------------

class Wheeled(Actor):
  def __init__(self, world, name, mesh, chassisType = None, body = None,
      **kargs):
    self.chassis = Actuator(name+"Chassis", chassisType, mesh, **kargs)
    
    Actor.__init__(self, world, name, actuator = self.chassis)
    
    bodyModel = mesh.find("**/"+body)
    if not bodyModel.isEmpty():
      self.body = Mesh(name+"Body", model = bodyModel, parent = self)
    else:
      framework.error("Body model '"+body+"' not found")
