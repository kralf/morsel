from node import Node

#-------------------------------------------------------------------------------

class Output(Node):
  def __init__(self, period = None, **kargs):
    super(Output, self).__init__(**kargs)
    
    framework.scheduler.addTask(self.name+"/Update", self.update,
      period = period)

#-------------------------------------------------------------------------------

  def update(self, time):
    self.send(time)
    return True

#-------------------------------------------------------------------------------

  def send(self, time):
    pass
