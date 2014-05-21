from morsel.panda import *
from morsel.nodes.facade import Mesh
from morsel.nodes.actuator import Actuator

#-------------------------------------------------------------------------------

class Drive(Actuator):
  def __init__(self, mesh = None, **kargs):
    super(Drive, self).__init__(**kargs)
   
    self.mesh = Mesh(filename = mesh, flatten = True)
    
#-------------------------------------------------------------------------------

  def setActuated(self, actuated):
    if self.actuated:
      self.detachNode()
      
    Actuator.setActuated(self, actuated)
    
    if self.actuated:
      self.parent = self.actuated
      self.clearTransform()

  actuated = property(Actuator.getActuated, setActuated)
  
#-------------------------------------------------------------------------------

  def getLinearVelocity(self):
    pass

  def setLinearVelocity(self, linearVelocity):
    pass

  linearVelocity = property(getLinearVelocity, setLinearVelocity)

#-------------------------------------------------------------------------------

  def getAngularVelocity(self):
    pass

  def setAngularVelocity(self, angularVelocity):
    pass

  angularVelocity = property(getAngularVelocity, setAngularVelocity)
    