from morsel.world.globals import *
from node import Node
from facade import Collider

#-------------------------------------------------------------------------------

class Platform(Node):
  def __init__(self, world, name, limits = [], **kargs):
    self.pose = [0, 0, 0, 0, 0, 0]

    Node.__init__(self, world, name, **kargs)

    self.collider = Collider(name+"Collider", parent = self,
      collisionMasks = [PLATFORM_COLLISIONS_FROM, PLATFORM_COLLISIONS_INTO])

    self._command = [0]*len(limits)
    self.limits = limits
    self.command = self._command
    self.state = [0]*len(limits)

#-------------------------------------------------------------------------------

  def setPosition(self, position):
    Node.setPosition(self, position)
    
    self.pose[0] = position[0]
    self.pose[1] = position[1]
    self.pose[2] = position[2]

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation):
    Node.setOrientation(self, orientation)
    
    self.pose[3] = orientation[0]
    self.pose[4] = orientation[1]
    self.pose[5] = orientation[2]

  orientation = property(Node.getOrientation, setOrientation)

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
    self.setPosition([self.pose[0], self.pose[1], self.pose[2]])
    self.setOrientation([self.pose[3], self.pose[4], self.pose[5]])
