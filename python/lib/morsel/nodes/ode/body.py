from morsel.panda import *
from morsel.math import *
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Body(Node):
  def __init__(self, world, name, solid, mass = None, position = [0, 0, 0],
      orientation = [0, 0, 0], **kargs):
    self.solid = solid
    self.mass = mass
    self.body = panda.OdeBody(world.world)

    if self.mass:
      self.body.setMass(self.mass)

    Node.__init__(self, world, name, position = position,
      orientation = orientation, **kargs)

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
      tv = node.getRelativeVector(self.world.scene, self.body.getLinearVel())
    else:
      tv = self.getRelativeVector(self.world.scene, self.body.getLinearVel())

    return [tv[0], tv[1], tv[2]]

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
      rv = node.getRelativeVector(self.world.scene,
        self.body.getAngularVel()*180/pi)
    else:
      rv = self.getRelativeVector(self.world.scene,
        self.body.getAngularVel()*180/pi)

    return [rv[2], rv[1], rv[0]]

  def setRotationalVelocity(self, rotationalVelocity, node = None):
    rv = [rotationalVelocity[2], rotationalVelocity[1], rotationalVelocity[0]]
    
    if node:
      self.body.setAngularVel(self.world.scene.getRelativeVector(node,
        panda.Vec3(*rv))*pi/180)
    else:
      self.body.setAngularVel(self.world.scene.getRelativeVector(self,
        panda.Vec3(*rv))*pi/180)

  rotationalVelocity = property(getRotationalVelocity, setRotationalVelocity)

#-------------------------------------------------------------------------------

  def setTorque(self, torque, node = None):
    if node:
      self.body.setTorque(self.world.scene.getRelativeVector(node,
        panda.Vec3(*torque)))
    else:
      self.body.setTorque(self.world.scene.getRelativeVector(self,
        panda.Vec3(*torque)))

#-------------------------------------------------------------------------------

  def updateTransform(self):
    self.body.setPosition(self.getPos(self.world.scene))
    self.body.setQuaternion(self.getQuat(self.world.scene))
