from node import Node

#-------------------------------------------------------------------------------

class Controller(Node):
  def __init__(self, actuator = None, platform = None, actor = None, **kargs):
    self._actuator = None
    
    super(Controller, self).__init__(**kargs)

    if actuator:
      self.actuator = actuator
    elif platform:
      self.platform = platform
    elif actor:
      self.actor = actor
    self.time = None
    
    framework.scheduler.addTask(self.name+"/Update", self.update)
    
#-------------------------------------------------------------------------------

  def getActuator(self):
    return self._actuator
    
  def setActuator(self, actuator):
    if self._actuator:
      self.detachNode()
      
    self._actuator = actuator
    
    if self._actuator:
      self.parent = self._actuator
    
  actuator = property(getActuator, setActuator)
  
#-------------------------------------------------------------------------------

  def setPlatform(self, platform):
    self.actuator = platform.actuator
    
  platform = property(None, setPlatform)
  
#-------------------------------------------------------------------------------

  def setActor(self, actor):
    self.actuator = actor.actuator
    
  actor = property(None, setActor)
  
#-------------------------------------------------------------------------------
  
  def update(self, time):
    if self.time and self.actuator:
      self.step(time-self.time)
          
    self.time = time
    return True

#-------------------------------------------------------------------------------

  def step(self, period):
    pass
