from morsel.core import *
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Geometry(Node):
  def __init__(self, world, name, solid, geometry, **kargs):
    self.solid = solid
    self.geometry = geometry

    Node.__init__(self, world, name, **kargs)

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)
    self.geometry.setPosition(self.getPos(self.world.scene))

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)
    self.geometry.setQuaternion(self.getQuat(self.world.scene))

  orientation = property(Node.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getBody(self):
    return self.geometry.getBody()

  def setBody(self, body):
    self.geometry.setBody(body)

  body = property(getBody, setBody)

#-------------------------------------------------------------------------------

  def getPositionOffset(self):
    return self.geometry.getOffsetPosition()

  def setPositionOffset(self, positionOffset):
    self.geometry.setOffsetPosition(*positionOffset)

  positionOffset = property(getPositionOffset, setPositionOffset)

#-------------------------------------------------------------------------------

  def setCollisionMasks(self, collisionMasks):
    self.geometry.setCategoryBits(collisionMasks[0])
    self.geometry.setCollideBits(collisionMasks[1])

#-------------------------------------------------------------------------------

  def update(self):
    self.setPosQuat(self.world.scene, self.geometry.getPosition(),
      self.geometry.getQuaternion())
