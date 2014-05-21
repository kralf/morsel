from morsel.panda import *
from morsel.morselc import Color

#-------------------------------------------------------------------------------

class Node(panda.NodePath):
  def __init__(self, world = None, name = None, parent = None, position = None,
      orientation = None, scale = None, color = None, hidden = False, **kargs):
    if not world:
      world = framework.world
    if not name:
      name = self.__class__.__name__
        
    super(Node, self).__init__(name)
        
    self.type = self.__class__
    self.this = self
    
    self.world = world
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
    d_xyz = panda.Vec3(*position)-panda.Vec3(*Node.getPosition(self, node))
    
    if node:
      panda.NodePath.setPos(self, node, *position)
    else:
      panda.NodePath.setPos(self, *position)
      
    self.onTransform(translation = [d_xyz[0], d_xyz[1], d_xyz[2]])

  position = property(getPosition, setPosition)

#-------------------------------------------------------------------------------

  def getX(self, node = None):
    if node:
      return panda.NodePath.getX(self, node)
    else:
      return panda.NodePath.getX(self)

  def setX(self, x, node = None):
    d_x = x-self.getX(node)
    
    if node:
      panda.NodePath.setX(self, node, x)
    else:
      panda.NodePath.setX(self, x)
    
    self.onTransform(translation = [d_x, 0, 0])
    
  x = property(getX, setX)
  
#-------------------------------------------------------------------------------

  def getY(self, node = None):
    if node:
      return panda.NodePath.getY(self, node)
    else:
      return panda.NodePath.getY(self)

  def setY(self, y, node = None):
    d_y = y-self.getY(node)
    
    if node:
      panda.NodePath.setY(self, node, y)
    else:
      panda.NodePath.setY(self, y)
      
    self.onTransform(translation = [0, d_y, 0])
    
  y = property(getY, setY)
  
#-------------------------------------------------------------------------------

  def getZ(self, node = None):
    if node:
      return panda.NodePath.getZ(self, node)
    else:
      return panda.NodePath.getZ(self)

  def setZ(self, z, node = None):
    d_z = z-self.getZ(node)
    
    if node:
      panda.NodePath.setZ(self, node, z)
    else:
      panda.NodePath.setZ(self, z)
      
    self.onTransform(translation = [0, 0, d_z])
    
  z = property(getZ, setZ)

#-------------------------------------------------------------------------------

  def getGlobalPosition(self):
    return self.getPosition(render)

  def setGlobalPosition(self, position):
    self.setPosition(position, render)

  globalPosition = property(getGlobalPosition, setGlobalPosition)

#-------------------------------------------------------------------------------

  def getOrientation(self, node = None):
    if node:
      orientation = self.getHpr(node)
    else:
      orientation = self.getHpr()
      
    return [orientation[0], orientation[2], orientation[1]]

  def setOrientation(self, orientation, node = None):
    d_ypr = (panda.Vec3(orientation[0], orientation[2], orientation[1])-
      panda.Vec3(*Node.getOrientation(self, node)))
    
    if node:
      self.setHpr(node, orientation[0], orientation[2], orientation[1])
    else:
      self.setHpr(orientation[0], orientation[2], orientation[1])
      
    self.onTransform(rotation = [d_ypr[0], d_ypr[1], d_ypr[2]])

  orientation = property(getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getYaw(self, node = None):
    if node:
      return panda.NodePath.getH(self, node)
    else:
      return panda.NodePath.getH(self)

  def setYaw(self, yaw, node = None):
    d_yaw = yaw-self.getYaw(node)
    
    if node:
      panda.NodePath.setH(self, node, yaw)
    else:
      panda.NodePath.setH(self, yaw)
      
    self.onTransform(rotation = [d_yaw, 0, 0])

  yaw = property(getYaw, setYaw)
  
#-------------------------------------------------------------------------------

  def getPitch(self, node = None):
    if node:
      return panda.NodePath.getR(self, node)
    else:
      return panda.NodePath.getR(self)

  def setPitch(self, pitch, node = None):
    d_pitch = pitch-self.getPitch(node)
    
    if node:
      panda.NodePath.setR(self, node, pitch)
    else:
      panda.NodePath.setR(self, pitch)
      
    self.onTransform(rotation = [0, d_pitch, 0])

  pitch = property(getPitch, setPitch)
  
#-------------------------------------------------------------------------------

  def getRoll(self, node = None):
    if node:
      return panda.NodePath.getP(self, node)
    else:
      return panda.NodePath.getP(self)

  def setRoll(self, roll, node = None):
    d_roll = roll-self.getRoll(node)
    
    if node:
      panda.NodePath.setP(self, node, roll)
    else:
      panda.NodePath.setP(self, roll)
      
    self.onTransform(rotation = [0, 0, d_roll])

  roll = property(getRoll, setRoll)

#-------------------------------------------------------------------------------

  def getGlobalOrientation(self):
    return self.getOrientation(render)

  def setGlobalOrientation(self, orientation):
    self.setOrientation(orientation, render)

  globalOrientation = property(getGlobalOrientation, setGlobalOrientation)

#-------------------------------------------------------------------------------

  def getQuaternion(self, node = None):
    if node:
      return self.getQuat(node)
    else:
      return self.getQuat()

  def setQuaternion(self, quaternion, node = None):
    d_quat = self.getQuaternion(node).conjugate()*quaternion
    d_hpr = d_quat.getHpr()
    
    if node:
      self.setQuat(node, quaternion)
    else:
      self.setQuat(quaternion)
    
    self.onTransform(rotation = [d_hpr[0], d_hpr[2], d_hpr[1]])

  quaternion = property(getQuaternion, setQuaternion)

#-------------------------------------------------------------------------------

  def getGlobalQuaternion(self):
    return self.getQuaternion(render)

  def setGlobalQuaternion(self, quaternion):
    self.setQuaternion(quaternion, render)

  globalQuaternion = property(getGlobalQuaternion, setGlobalQuaternion)

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

    s_xyz = Node.getScale(self, node)
    for i in range(len(s_xyz)):
      if s_xyz[i]:
        s_xyz[i] = scale[i]/s_xyz[i]
      else:
        s_xyz[i] = float("nan")
      
    if node:
      panda.NodePath.setScale(self, node, *scale)
    else:
      panda.NodePath.setScale(self, *scale)
    
    self.onTransform(scaling = s_xyz)

  scale = property(getScale, setScale)

#-------------------------------------------------------------------------------

  def getGlobalScale(self):
    return self.getScale(render)

  def setGlobalScale(self, scale):
    self.setScale(scale, render)

  globalScale = property(getGlobalScale, setGlobalScale)

#-------------------------------------------------------------------------------

  def getMatrix(self, node = None):
    if node:
      M = panda.NodePath.getMat(self, node)
    else:
      M = panda.NodePath.getMat(self)
      
    return [[M(0, 0), M(0, 1), M(0, 2), M(0, 3)],
            [M(1, 0), M(1, 1), M(1, 2), M(1, 3)],
            [M(2, 0), M(2, 1), M(2, 2), M(2, 3)],
            [M(3, 0), M(3, 1), M(3, 2), M(3, 3)]]
    
  def setMatrix(self, M, node = None):
    M = panda.Mat4(M[0][0], M[0][1], M[0][2], M[0][3],
                   M[1][0], M[1][1], M[1][2], M[1][3],
                   M[2][0], M[2][1], M[2][2], M[2][3],
                   M[3][0], M[3][1], M[3][2], M[3][3])
                   
    T = self.getTransform(node).invertCompose(
      panda.TransformState.makeMat(M))
      
    d_xyz = T.getPos()
    d_hpr = T.getHpr()
    s_xyz = T.getScale()

    if node:
      self.setMat(node, M)
    else:
      self.setMat(M)
      
    self.onTransform(
      translation = [d_xyz[0], d_xyz[1], d_xyz[2]],
      rotation = [d_hpr[0], d_hpr[2], d_hpr[1]],
      scaling = [s_xyz[0], s_xyz[1], s_xyz[2]])

  matrix = property(getMatrix, setMatrix)

#-------------------------------------------------------------------------------

  def getGlobalMatrix(self):
    return self.getMatrix(render)

  def setGlobalMatrix(self, M):
    self.setMatrix(M, render)

  globalMatrix = property(getGlobalMatrix, setGlobalMatrix)

#-------------------------------------------------------------------------------

  def getTransform(self, node = None):
    if node:
      return panda.NodePath.getTransform(self, node)
    else:
      return panda.NodePath.getTransform(self)
    
  def setTransform(self, transform, node = None):
    T = self.getTransform(node).invertCompose(transform)
    
    d_xyz = T.getPos()
    d_hpr = T.getHpr()
    s_xyz = T.getScale()
    
    if node:
      panda.NodePath.setTransform(self, node, transform)
    else:
      panda.NodePath.setTransform(self, transform)
      
    self.onTransform(
      translation = [d_xyz[0], d_xyz[1], d_xyz[2]],
      rotation = [d_hpr[0], d_hpr[2], d_hpr[1]],
      scaling = [s_xyz[0], s_xyz[1], s_xyz[2]])

  transform = property(getTransform, setTransform)

#-------------------------------------------------------------------------------

  def getGlobalTransform(self):
    return self.getTransform(render)

  def setGlobalTransform(self, transform):
    self.setTransform(transform, render)

  globalTransform = property(getGlobalTransform, setGlobalTransform)

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

  def getLabel(self, name):
    return Color.rgbToInt(self.getShaderInput(name).getVector())

  def setLabel(self, name, label):
    self.setShaderInput(name, Color.intToRgb(label))

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

  def getBounds(self, node = None):
    p_min = panda.Point3()
    p_max = panda.Point3()
    q_min = panda.Point3()
    q_max = panda.Point3()
    
    for i in range(0, self.getNumChildren()):
      child = self.getChild(i)
      
      if p_min and p_max:
        if child.calcTightBounds(q_min, q_max):
          p_min = p_min.fmin(q_min)
          p_max = p_max.fmax(q_max)
      else:
        child.calcTightBounds(p_min, p_max)

    if node:
      p_min = node.getRelativePoint(self, p_min)
      p_max = node.getRelativePoint(self, p_max)
      
    return (p_min, p_max)

  bounds = property(getBounds)

#-------------------------------------------------------------------------------

  def getGlobalBounds(self):
    return self.getBounds(render)

  globalBounds = property(getGlobalBounds)

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

  def setParent(self, parent):
    if not parent:
      parent = self.world.scene
      
    self.reparentTo(parent)

  parent = property(getParent, setParent)

#-------------------------------------------------------------------------------

  def getChildren(self, type = None):
    if not type:
      type = Node
      
    for i in range(0, self.getNumChildren()):
      child = self.getChild(i)      
      childType = child.getPythonTag("type")
      if childType and issubclass(childType, type):
        yield child.getPythonTag("this")

  children = property(getChildren)

#-------------------------------------------------------------------------------

  def translate(self, translation, node = None):
    if not node:
      node = self
    
    d_xyz = self.parent.getRelativeVector(node, panda.Vec3(*translation))
    panda.NodePath.setPos(self, panda.NodePath.getPos(self)+d_xyz)
    
    self.onTransform(translation = [d_xyz[0], d_xyz[1], d_xyz[2]])

#-------------------------------------------------------------------------------

  def rotate(self, rotation, node = None):
    if not node:
      node = self
      
    if node != self:
      position = panda.NodePath.getPos(self, node)
      
      d_quat = panda.Quat()
      d_quat.setHpr(panda.Vec3(rotation[0], rotation[2], rotation[1]))
      d_xyz = self.parent.getRelativeVector(node,
        d_quat.xform(position)-position)
      d_hpr = d_quat.getHpr()
      
      panda.NodePath.setPosQuat(self, panda.NodePath.getPos(self)+d_xyz,
        d_quat*panda.NodePath.getQuat(self))
        
      self.onTransform(translation = [d_xyz[0], d_xyz[1], d_xyz[2]],
        rotation = [d_hpr[0], d_hpr[2], d_hpr[1]])      
    else:
      d_quat = panda.Quat()
      d_quat.setHpr(panda.Vec3(rotation[0], rotation[2], rotation[1]))
      
      panda.NodePath.setQuat(self, d_quat*panda.NodePath.getQuat(self))
      
      self.onTransform(rotation = rotation)      

#-------------------------------------------------------------------------------

  def applyTransform(self, node = None):
    if node:
      transform = panda.NodePath.getTransform(self, node)
    else:
      transform = panda.NodePath.getTransform(self)
    
    for i in range(0, self.getNumChildren()):
      child = self.getChild(i)
      childType = child.getPythonTag("type")
      if childType and issubclass(childType, Node):
        child = child.getPythonTag("this")
        
      child.setTransform(child.getTransform().invertCompose(transform))
    
    self.setTransform(self.transform.compose(transform))
    
#-------------------------------------------------------------------------------

  def clearTransform(self, node = None):
    if node:
      T = panda.NodePath.getTransform(self, node).getInverse()
      panda.NodePath.clearTransform(self, node)
    else:
      T = panda.NodePath.getTransform(self).getInverse()
      panda.NodePath.clearTransform(self)
      
    d_xyz = T.getPos()
    d_hpr = T.getHpr()
    s_xyz = T.getScale()
    
    self.onTransform(
      translation = [d_xyz[0], d_xyz[1], d_xyz[2]],
      rotation = [d_hpr[0], d_hpr[2], d_hpr[1]],
      scaling = [s_xyz[0], s_xyz[1], s_xyz[2]])

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
    framework.base.mouseInterfaceNode.setMat(matrix)
    
    if rotate == False:
      camera.setEffect(panda.CompassEffect.make(render))
      
#-------------------------------------------------------------------------------

  def toggleShow(self):
    self.hidden = not self.hidden
    
#-------------------------------------------------------------------------------

  def onTransform(self, translation = None, rotation = None, scaling = None):
    if translation:
      self.onTranslate(translation)
    if rotation:
      self.onRotate(rotation)
    if scaling:
      self.onScale(scaling)

#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    pass

#-------------------------------------------------------------------------------

  def onRotate(self, rotation):
    pass

#-------------------------------------------------------------------------------

  def onScale(self, scaling):
    pass
    