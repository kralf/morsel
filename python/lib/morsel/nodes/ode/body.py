from morsel.core import *
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Body(Node):
  def __init__(self, world, name, solid, mass = None, **kargs):
    self.solid = solid
    self.body = panda.OdeBody(world.world)
    self.mass = mass

    if self.mass:
      self.body.setMass(self.mass)
    if self.solid.geometry:
      self.solid.geometry.body = self.body

    Node.__init__(self, world, name, **kargs)

#-------------------------------------------------------------------------------

  def setPosition(self, position):
    Node.setPosition(self, position)
    self.body.setPosition(self.getPos(self.world.scene))

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation):
    Node.setOrientation(self, orientation)
    self.body.setQuaternion(self.getQuat(self.world.scene))

  orientation = property(Node.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def update(self):
    self.setPosQuat(self.world.scene, self.body.getPosition(),
      panda.Quat(self.body.getQuaternion()))
