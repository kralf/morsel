from object import Object

#-------------------------------------------------------------------------------

class Actuated(Object):
  def __init__(self, actuator = None, **kargs):
    self._actuator = None
    
    super(Actuated, self).__init__(**kargs)

    self.actuator = actuator

#-------------------------------------------------------------------------------

  def getActuator(self):
    return self._actuator
    
  def setActuator(self, actuator):
    if self._actuator:
      self._actuator.actuated = None
      
    self._actuator = actuator
    
    if self._actuator:
      self._actuator.actuated = self
  
  actuator = property(getActuator, setActuator)
  