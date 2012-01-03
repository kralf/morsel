from morsel.panda import *

#-------------------------------------------------------------------------------

class Node(panda.NodePath):
  def __init__(self, name, parent = None, position = None, orientation = None,
      scale = None, color = None, hidden = False, **kargs):
    panda.NodePath.__init__(self, name)
        
    self.type = self.__class__
    self.this = self
    
    self.parent = parent

    if position:
      self.position = position
    if orientation:
      self.orientation = orientation
    if scale:
      self.scale = scale
    if color:
      self.color = color
    if hidden:
      self.hidden = hidden

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

  def getQuaternion(self, node = None):
    if node:
      return self.getQuat(node)
    else:
      return self.getQuat()

  def setQuaternion(self, quaternion, node = None):
    if node:
      self.setQuat(node, quaternion)
    else:
      self.setQuat(quaternion)

  quaternion = property(getQuaternion, setQuaternion)

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
      scale = panda.NodePath.getScale(self, node)
    else:
      scale = panda.NodePath.getScale(self)
      
    return [scale[0], scale[1], scale[2]]
    
  def setScale(self, scale, node = None):
    if not isinstance(scale, list):
      scale = [scale]*3
      
    if node:
      panda.NodePath.setScale(self, node, *scale)
    else:
      panda.NodePath.setScale(self, *scale)

  scale = property(getScale, setScale)

#-------------------------------------------------------------------------------

  def getBounds(self, node = None):
    p_min = panda.Point3()
    p_max = panda.Point3()
    if not self.calcTightBounds(p_min, p_max):
      p_min = panda.Point3(*self.position)
      p_max = panda.Point3(*self.position)

    if not node:
      node = self
    p_min = node.getRelativePoint(self.parent, p_min)
    p_max = node.getRelativePoint(self.parent, p_max)

    return (p_min, p_max)

  bounds = property(getBounds)

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

  def getHidden(self):
    return self.isHidden()

  def setHidden(self, hidden):
    if hidden and not self.hidden:
      self.hide()
    elif self.hidden:
      self.show()

  hidden = property(getHidden, setHidden)

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
    parent = panda.NodePath.getParent(self)

    if parent.hasPythonTag("this"):
      return parent.getPythonTag("this")
    else:
      return parent

  def setParent(self, parent, transform = False):
    if not parent:
      parent = render
      
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

  def toggle(self):
    self.hidden = not self.hidden
