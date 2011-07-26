from node import Node

#-------------------------------------------------------------------------------

class Platform(Node):
  def __init__(self, world, name, limits = [], **kargs):
    Node.__init__(self, world, name, **kargs)

    self._command = [0]*len(limits)

    self.limits = limits
    self.command = self._command
    self.state = self.command

#-------------------------------------------------------------------------------

  def getCommand(self):
    return self._command

  def setCommand(self, command):
    for i in range(min(len(self.limits), len(command))):
      self._command[i] = max(self.limits[i][0],
        min(self.limits[i][1], command[i]))

  command = property(getCommand, setCommand)
  
#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    pass

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    pass
