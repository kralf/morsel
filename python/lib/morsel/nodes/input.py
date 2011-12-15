from node import Node

#-------------------------------------------------------------------------------

class Input(Node):
  def __init__(self, name, period = None, **kargs):
    Node.__init__(self, name, **kargs)
    framework.scheduler.addTask(name+"Update", self.update, period = period)

#-------------------------------------------------------------------------------

  def update(self, time):
    self.inputData(time)
    return True

#-------------------------------------------------------------------------------

  def inputData(self, time):
    pass
