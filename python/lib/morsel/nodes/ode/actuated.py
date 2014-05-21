from morsel.nodes.actuated import Actuated as Base
from object import Object

#-------------------------------------------------------------------------------

class Actuated(Object, Base):
  def __init__(self, **kargs):
    super(Actuated, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def setBody(self, body):
    Object.setBody(self, body)
    
    self.actuator = self._actuator
    
  body = property(Object.getBody, setBody)
  