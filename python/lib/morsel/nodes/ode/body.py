from morsel.panda import *
from morsel.math import *
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

  def getTranslationalVelocity(self, node = None):
    if node:
      dt = node.getRelativeVector(self.world.scene, self.body.getLinearVel())
    else:
      dt = self.getRelativeVector(self.world.scene, self.body.getLinearVel())

    return [dt[0], dt[1], dt[2]]

  def setTranslationalVelocity(self, translationalVelocity, node = None):
    if node:
      self.body.setLinearVel(self.world.scene.getRelativeVector(node,
        panda.Vec3(*translationalVelocity)))
    else:
      self.body.setLinearVel(self.world.scene.getRelativeVector(self,
        panda.Vec3(*translationalVelocity)))

  translationalVelocity = property(getTranslationalVelocity,
    setTranslationalVelocity)

#-------------------------------------------------------------------------------

  def getRotationalVelocity(self, node = None):
    if node:
      dr = node.getRelativeVector(self.world.scene,
        self.body.getAngularVel()*180/pi)
    else:
      dr = self.getRelativeVector(self.world.scene,
        self.body.getLinearVel()*180/pi)

    return [dr[0], dr[1], dr[2]]

  def setRotationalVelocity(self, rotationalVelocity, node = None):
    if node:
      self.body.setAngularVel(self.world.scene.getRelativeVector(node,
        panda.Vec3(*rotationalVelocity))*pi/180)
    else:
      self.body.setAngularVel(self.world.scene.getRelativeVector(self,
        panda.Vec3(*rotationalVelocity))*pi/180)

  rotationalVelocity = property(getRotationalVelocity, setRotationalVelocity)
