from node import Node

#-------------------------------------------------------------------------------

class Controller(Node):
  def __init__(self, world, name, platform = None, **kargs):
    Node.__init__(self, world, name, **kargs)
    
    self.platform = platform
    self.time = None
    
    framework.scheduler.addTask(name+"ControllerUpdate", self.update)
    
#-------------------------------------------------------------------------------
  
  def update(self, time):
    if self.time and self.platform:
      self.updateCommand(time-self.time)
          
    self.time = time
    return True

#-------------------------------------------------------------------------------

  def updateCommand(self, period):
    pass
