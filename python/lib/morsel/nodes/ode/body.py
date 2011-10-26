from morsel.core import *
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Body(Node):
  def __init__(self, world, name, solid = None, mass = None,
      position = [0, 0, 0], massOffset = [0, 0, 0], **kargs):
    self.solid = solid
    self.body = panda.OdeBody(world.world)
    self.mass = mass

    if self.mass:
      self.body.setMass(self.mass)
    if self.solid and self.solid.geometry:
      self.solid.geometry.body = self.body
      self.solid.geometry.positionOffset = [-p_i for p_i in massOffset]

    for i in range(len(position)):
      position[i] += massOffset[i]

    Node.__init__(self, world, name, position = position, **kargs)

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)
    self.body.setPosition(self.getPos(self.world.scene))

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)
    self.body.setQuaternion(self.getQuat(self.world.scene))

  orientation = property(Node.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def update(self):
    self.setPosQuat(self.world.scene, self.body.getPosition(),
      panda.Quat(self.body.getQuaternion()))
