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
    self._translationalVelocity = [0, 0, 0]
    self._rotationalVelocity = [0, 0, 0]
    self.limits = limits
    self.command = self._command
    self.state = [0]*len(limits)

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)
    
    self.pose[0] = self.position[0]
    self.pose[1] = self.position[1]
    self.pose[2] = self.position[2]

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)
    
    self.pose[3] = self.orientation[0]
    self.pose[4] = self.orientation[1]
    self.pose[5] = self.orientation[2]

  orientation = property(Node.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getTranslationalVelocity(self):
    pass

  def setTranslationalVelocity(self, translationalVelocity):
    pass

  translationalVelocity = property(getTranslationalVelocity,
    setTranslationalVelocity)
  
#-------------------------------------------------------------------------------

  def getRotationalVelocity(self):
    pass

  def setRotationalVelocity(self, rotationalVelocity):
    pass

  rotationalVelocity = property(getRotationalVelocity, setRotationalVelocity)

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
