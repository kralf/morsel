from morsel.panda import *
from morsel.nodes import Platform
from morsel.nodes.facade import Mesh
from morsel.platforms.facade import Actuator

#-------------------------------------------------------------------------------

class Wheeled(Platform):
  def __init__(self, world, name, mesh, chassisType = None, body = None,
      **kargs):
    self.chassis = Actuator(name = name+"Chassis", type = chassisType,
      mesh = mesh, **kargs)
    
    Platform.__init__(self, world, name, actuator = self.chassis)
    
    bodyModel = mesh.find("**/"+body)
    if not bodyModel.isEmpty():
      self.body = Mesh(name = name+"Body", model = bodyModel, parent = self)
    else:
      framework.error("Body model '"+body+"' not found")
