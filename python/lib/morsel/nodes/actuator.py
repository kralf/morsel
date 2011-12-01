from morsel.world.globals import *
from node import Node
from facade import Collider, Solid

#-------------------------------------------------------------------------------

class Actuator(Node):
  def __init__(self, world, name, solid = None, limits = [], **kargs):
    self.solid = None
    
    Node.__init__(self, world, name, **kargs)

    self.collider = Collider(name = name+"Collider", parent = self,
      collisionMasks = [ACTUATOR_COLLISIONS_FROM, ACTUATOR_COLLISIONS_INTO])
    if solid:
      self.solid = solid
    else:
      self.solid = Solid(name = name+"Solid", type = "Empty", mesh = self,
        parent = self)

    self.limits = limits
    self.command = [0]*len(limits)
    self.state = [0]*len(limits)

#-------------------------------------------------------------------------------

  def getPosition(self, node = None):
    if self.solid:
      if not node:
        node = self.parent
      return self.solid.getPosition(node)
    else:
      return Node.getPosition(self, node)

  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)

    if self.solid:
      self.solid.position = self.solid.position

  position = property(getPosition, setPosition)

#-------------------------------------------------------------------------------

  def getOrientation(self, node = None):
    if self.solid:
      if not node:
        node = self.parent
      return self.solid.getOrientation(node)
    else:
      return Node.getOrientation(self, node)

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)

    if self.solid:
      self.solid.orientation = self.solid.orientation

  orientation = property(getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getCommand(self):
    return self._command

  def setCommand(self, command):
    self._command = [0]*len(self.limits)
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
