from node import Node

#-------------------------------------------------------------------------------

class Output(Node):
  def __init__(self, world, name, period = None, **kargs):
    Node.__init__(self, world, name, **kargs)
    framework.scheduler.addTask(name+"Update", self.update, period = period)

#-------------------------------------------------------------------------------

  def update(self, time):
    self.outputData(time)
    return True

#-------------------------------------------------------------------------------

  def outputData(self, time):
    pass
