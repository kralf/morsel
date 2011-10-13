from morsel.core import *

#-------------------------------------------------------------------------------

class Controller(object):
  def __init__(self, name, platform = None):
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
