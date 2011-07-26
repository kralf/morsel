from morsel.core import *
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Geometry(Node):
  def __init__(self, world, name, solid, geometry, **kargs):
    self.solid = solid
    self.geometry = geometry

    Node.__init__(self, world, name, **kargs)

#-------------------------------------------------------------------------------

  def setPosition(self, position):
    Node.setPosition(self, position)
    self.geometry.setPosition(self.getPos(self.world.scene))

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation):
    Node.setOrientation(self, orientation)
    self.geometry.setQuaternion(self.getQuat(self.world.scene))

  orientation = property(Node.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getBody(self):
    if self.geometry:
      return self.geometry.getBody()
    else:
      return None

  def setBody(self, body):
    if self.geometry:
      self.geometry.setBody(body)

  body = property(getBody, setBody)

#-------------------------------------------------------------------------------

  def setCollisionMasks(self, collisionsFrom, collisionsInto):
    self.geometry.setCategoryBits(collisionsFrom)
    self.geometry.setCollideBits(collisionsInto)

#-------------------------------------------------------------------------------

  def update(self):
    self.setPosQuat(self.world.scene, self.geometry.getPosition(),
      self.geometry.getQuaternion())
