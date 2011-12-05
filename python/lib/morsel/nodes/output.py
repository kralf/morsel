from node import Node

#-------------------------------------------------------------------------------

class Output(Node):
  def __init__(self, world, name, source = None, period = None, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.source = source
    self.time = None

    framework.scheduler.addTask(name+"Update", self.update, period = period)

#-------------------------------------------------------------------------------

  def update(self, time):
    if self.source:
      self.outputData(time)

    return True

#-------------------------------------------------------------------------------

  def outputData(self, time):
    pass
