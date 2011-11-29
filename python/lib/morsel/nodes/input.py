from node import Node

#-------------------------------------------------------------------------------

class Input(Node):
  def __init__(self, world, name, destination = None, period = None, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.destination = destination
    self.time = None

    framework.scheduler.addTask(name+"Update", self.update, period = period)

#-------------------------------------------------------------------------------

  def update(self, time):
    if self.time and self.destination:
      self.inputData(time-self.time)

    self.time = time
    return True

#-------------------------------------------------------------------------------

  def inputData(self, period):
    pass
