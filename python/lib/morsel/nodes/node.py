from morsel.core import *
from morsel.morselc import Color

import sys

#-------------------------------------------------------------------------------

class Node(panda.NodePath):
  def __init__(self, world, name, parent = None, position = [0, 0, 0],
      orientation = [0, 0, 0], scale = 1, **kargs):
    panda.NodePath.__init__(self, name)

    if not world:
      raise RuntimeError( "World not initialized" )

    self.type = self.__class__
    self.this = self
    self.world = world
    self.world.registerNode(self)

    self.parent = parent
    self.position = position
    self.orientation = orientation
    self.scale = scale

#-------------------------------------------------------------------------------

  name = property(panda.NodePath.getName, panda.NodePath.setName)

#-------------------------------------------------------------------------------

  def getPosition(self):
    return [self.getX(), self.getY(), self.getZ()]

  def setPosition(self, position):
    self.setPos(*position)

  position = property(getPosition, setPosition)

#-------------------------------------------------------------------------------

  x = property(panda.NodePath.getX, panda.NodePath.setX)
  y = property(panda.NodePath.getY, panda.NodePath.setY)
  z = property(panda.NodePath.getZ, panda.NodePath.setZ)

#-------------------------------------------------------------------------------

  def getOrientation(self):
    return [self.getH(), self.getP(), self.getR()]

  def setOrientation(self, orientation):
    self.setHpr(*orientation)

  orientation = property(getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  yaw = property(panda.NodePath.getH, panda.NodePath.setH)
  pitch = property(panda.NodePath.getP, panda.NodePath.setP)
  roll = property(panda.NodePath.getR, panda.NodePath.setR)

#-------------------------------------------------------------------------------

  def setScale(self, scale):
    if isinstance(scale, list):
      panda.NodePath.setScale(self, *scale)
    else:
      panda.NodePath.setScale(self, scale)

  scale = property(panda.NodePath.getScale, setScale)

#-------------------------------------------------------------------------------

  def setTransformFromPath(self, node):
    self.setPos(node.getPos(self))
    self.setHpr(node.getHpr(self))

#-------------------------------------------------------------------------------

  def getRelativePosition(self, node, position):
    relative = self.getRelativePoint(node, panda.Vec3(*position))
    return [relative[0], relative[1], relative[2]]

#-------------------------------------------------------------------------------

  def getLabel(self, name):
    return Color.rgbToInt(self.getShaderInput(name).getVector())

  def setLabel(self, name, label):
    self.setShaderInput(name, Color.intToRgb(label))

#-------------------------------------------------------------------------------

  def getProperty(self, name):
    if self.hasPythonTag(name):
      return self.getPythonTag(name)
    else:
      return None

  def setProperty(self, name, value):
    self.setPythonTag(name, value)

#-------------------------------------------------------------------------------

  def getType(self):
    return self.getProperty("type")

  def setType(self, type):
    return self.setProperty("type", type)

  type = property(getType, setType)

#-------------------------------------------------------------------------------

  def getThis(self):
    return self.getProperty("this")

  def setThis(self, this):
    return self.setProperty("this", this)

  this = property(getThis, setThis)

#-------------------------------------------------------------------------------

  def getParent(self):
    return panda.NodePath.getParent(self).getPythonTag("this")

  def setParent(self, parent, transform = False):
    if not parent:
      parent = self.world.scene

    if transform:
      self.setTransform(self.getTransform(parent))
    
    self.reparentTo(parent)

  parent = property(getParent, setParent)

#-------------------------------------------------------------------------------

  def getCollider(self):
    return self.getProperty("collider")

  def setCollider(self, collider):
    return self.setProperty("collider", collider)

  collider = property(getCollider, setCollider)

#-------------------------------------------------------------------------------

  def attachCamera(self, position, lookAt = [0, 0, 0], camera = None,
      rotate = False):
    if not camera:
      camera = framework.base.camera
      
    camera.reparentTo(self)
    camera.setPos(*position)
    camera.lookAt(*lookAt)
    
    matrix = panda.Mat4(camera.getMat())
    matrix.invertInPlace()
    base.mouseInterfaceNode.setMat(matrix)
    
    if rotate == False:
      camera.setEffect(panda.CompassEffect.make(self.world.scene))
