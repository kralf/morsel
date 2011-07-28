from morsel.world.globals import *
from node import Node
from facade import Collider

#-------------------------------------------------------------------------------

class Platform(Node):
  def __init__(self, world, name, limits = [], **kargs):
    Node.__init__(self, world, name, **kargs)

    self.collider = Collider(name+"Collider", parent = self,
      collisionMasks = [PLATFORM_COLLISIONS_FROM, PLATFORM_COLLISIONS_INTO])

    self._command = [0]*len(limits)
    self.limits = limits
    self.command = self._command
    self.state = [0]*len(limits)

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
