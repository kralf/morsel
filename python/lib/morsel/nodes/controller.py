from node import Node

#-------------------------------------------------------------------------------

class Controller(Node):
  def __init__(self, world, name, actuator = None, platform = None,
      actor = None, **kargs):
    Node.__init__(self, world, name, **kargs)

    if platform:
      self.actuator = platform.actuator
    elif actor:
      self.actuator = actor.actuator
    else:
      self.actuator = actuator
    self.time = None
    
    framework.scheduler.addTask(name+"Update", self.update)
    
#-------------------------------------------------------------------------------
  
  def update(self, time):
    if self.time and self.actuator:
      self.updateCommand(time-self.time)
          
    self.time = time
    return True

#-------------------------------------------------------------------------------

  def updateCommand(self, period):
    pass
