from morsel.core import *
from morsel.morselc import Color

import sys

#-------------------------------------------------------------------------------

class Node(panda.NodePath):
  def __init__(self, world, name, parent = None, position = None,
      orientation = None, scale = None, color = None, **kargs):
    panda.NodePath.__init__(self, name)
        
    if not world:
      raise RuntimeError( "World not initialized" )

    self.type = self.__class__
    self.this = self
    self.world = world
    self.world.registerNode(self)

    self.parent = parent

    if position:
      self.position = position
    if orientation:
      self.orientation = orientation
    if scale:
      self.scale = scale
    if color:
      self.color = color

#-------------------------------------------------------------------------------

  name = property(panda.NodePath.getName, panda.NodePath.setName)

#-------------------------------------------------------------------------------

  def getPosition(self, node = None):
    if node:
      position = self.getPos(node)
    else:
      position = self.getPos()
      
    return [position[0], position[1], position[2]]

  def setPosition(self, position, node = None):
    if node:
      self.setPos(node, *position)
    else:
      self.setPos(*position)

  position = property(getPosition, setPosition)

#-------------------------------------------------------------------------------

  x = property(panda.NodePath.getX, panda.NodePath.setX)
  y = property(panda.NodePath.getY, panda.NodePath.setY)
  z = property(panda.NodePath.getZ, panda.NodePath.setZ)

#-------------------------------------------------------------------------------

  def getGlobalPosition(self):
    return self.getPosition(self.world.scene)

  def setGlobalPosition(self, position):
    self.setPosition(position, self.world.scene)

  globalPosition = property(getGlobalPosition, setGlobalPosition)

#-------------------------------------------------------------------------------

  def getOrientation(self, node = None):
    if node:
      orientation = self.getHpr(node)
    else:
      orientation = self.getHpr()
      
    return [orientation[0], orientation[1], orientation[2]]

  def setOrientation(self, orientation, node = None):
    if node:
      self.setHpr(node, *orientation)
    else:
      self.setHpr(*orientation)

  orientation = property(getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  yaw = property(panda.NodePath.getH, panda.NodePath.setH)
  pitch = property(panda.NodePath.getP, panda.NodePath.setP)
  roll = property(panda.NodePath.getR, panda.NodePath.setR)

#-------------------------------------------------------------------------------

  def getGlobalOrientation(self):
    return self.getOrientation(self.world.scene)

  def setGlobalOrientation(self, orientation):
    self.setOrientation(orientation, self.world.scene)

  globalOrientation = property(getGlobalOrientation, setGlobalOrientation)

#-------------------------------------------------------------------------------

  def getHeading(self, node = None):
    quaternion = panda.Quat()
    quaternion.setHpr(panda.Vec3(*self.getOrientation(node)))
    heading = quaternion.xform(panda.Vec3(1, 0, 0))

    return [heading[0], heading[1], heading[2]]

  heading = property(getHeading)

#-------------------------------------------------------------------------------

  def getScale(self, node = None):
    if node:
      scale = panda.NodePath.getScale(node)
    else:
      scale = panda.NodePath.getScale()
      
    return [scale[0], scale[1], scale[2]]
    
  def setScale(self, scale, node = None):
    if not isinstance(scale, list):
      scale = [scale]*3
      
    if node:
      panda.NodePath.setScale(node, *scale)
    else:
      panda.NodePath.setScale(self, *scale)

  scale = property(getScale, setScale)

#-------------------------------------------------------------------------------

  def getColor(self):
    if self.hasColor():
      color = panda.NodePath.getColor(self)
      return [color[0], color[1], color[2], color[3]]
    else:
      return [0]*4

  def setColor(self, color):
    panda.NodePath.setColor(self, *color)

  color = property(getColor, setColor)

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

  def getChildren(self, type = None):
    if not type:
      type = Node
      
    for i in range(0, self.getNumChildren()):
      node = self.getChild(i)      
      childType = node.getPythonTag("type")
      if childType and issubclass(childType, type):
        yield node.getPythonTag("this")

  children = property(getChildren)

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
