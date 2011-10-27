from morsel.world.globals import *
from actor import Actor
from facade import Collider

#-------------------------------------------------------------------------------

class Platform(Actor):
  def __init__(self, world, name, limits = [], collisionMasks =
      [PLATFORM_COLLISIONS_FROM, PLATFORM_COLLISIONS_INTO], **kargs):
    self.pose = [0, 0, 0, 0, 0, 0]

    Actor.__init__(self, world, name, collisionMasks = collisionMasks, **kargs)

    self._command = [0]*len(limits)
    self.limits = limits
    self.command = self._command
    self.state = [0]*len(limits)

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Actor.setPosition(self, position, node)
    
    self.pose[0] = self.position[0]
    self.pose[1] = self.position[1]
    self.pose[2] = self.position[2]

  position = property(Actor.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Actor.setOrientation(self, orientation, node)
    
    self.pose[3] = self.orientation[0]
    self.pose[4] = self.orientation[1]
    self.pose[5] = self.orientation[2]

  orientation = property(Actor.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getCommand(self):
    return self._command

  def setCommand(self, command):
    for i in range(min(len(self.limits), len(command))):
      self._command[i] = max(self.limits[i][0],
        min(self.limits[i][1], command[i]))

  command = property(getCommand, setCommand)
  
#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.setPosition([self.pose[0], self.pose[1], self.pose[2]])
    self.setOrientation([self.pose[3], self.pose[4], self.pose[5]])
