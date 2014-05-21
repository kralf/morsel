from node import Node

#-------------------------------------------------------------------------------

class Input(Node):
  def __init__(self, period = None, **kargs):
    super(Input, self).__init__(**kargs)
    
    framework.scheduler.addTask(self.name+"/Update", self.update,
      period = period)

#-------------------------------------------------------------------------------

  def update(self, time):
    self.receive(time)
    return True

#-------------------------------------------------------------------------------

  def receive(self, time):
    pass
