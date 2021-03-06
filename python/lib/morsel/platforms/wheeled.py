from morsel.panda import *
from morsel.nodes.facade import Actuator, Mesh
from morsel.nodes.platform import Platform

#-------------------------------------------------------------------------------

class Wheeled(Platform):
  def __init__(self, name = None, actuator = None, bodyMesh = None, **kargs):
    super(Wheeled, self).__init__(name = name, **kargs)

    if bodyMesh:
      self.mesh = Mesh(filename = bodyMesh, flatten = True)
    self.actuator = Actuator(type = actuator, **kargs)
    