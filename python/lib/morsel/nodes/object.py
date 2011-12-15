from morsel.panda import *
from node import Node
from morsel.morselc import Color

#-------------------------------------------------------------------------------

class Object(Node):
  def __init__(self, world, name, **kargs):
    self.world = world
      
    Node.__init__(self, name, **kargs)
    
    self.world.registerObject(self)

#-------------------------------------------------------------------------------

  def getGlobalPosition(self):
    return self.getPosition(self.world.scene)

  def setGlobalPosition(self, position):
    self.setPosition(position, self.world.scene)

  globalPosition = property(getGlobalPosition, setGlobalPosition)

#-------------------------------------------------------------------------------

  def getGlobalOrientation(self):
    return self.getOrientation(self.world.scene)

  def setGlobalOrientation(self, orientation):
    self.setOrientation(orientation, self.world.scene)

  globalOrientation = property(getGlobalOrientation, setGlobalOrientation)

#-------------------------------------------------------------------------------

  def getGlobalQuaternion(self):
    return self.getQuaternion(self.world.scene)

  def setGlobalQuaternion(self, quaternion):
    self.setQuaternion(quaternion, self.world.scene)

  globalQuaternion = property(getGlobalQuaternion, setGlobalQuaternion)

#-------------------------------------------------------------------------------

  def getGlobalScale(self):
    return self.getScale(self.world.scene)

  def setGlobalScale(self, scale):
    self.setScale(scale, self.world.scene)

  globalScale = property(getGlobalScale, setGlobalScale)

#-------------------------------------------------------------------------------

  def getGlobalBounds(self):
    return self.getBounds(self.world.scene)

  globalBounds = property(getGlobalBounds)

#-------------------------------------------------------------------------------

  def getLabel(self, name):
    return Color.rgbToInt(self.getShaderInput(name).getVector())

  def setLabel(self, name, label):
    self.setShaderInput(name, Color.intToRgb(label))

#-------------------------------------------------------------------------------

  def setParent(self, parent, transform = False):
    if not parent:
      parent = self.world.scene

    Node.setParent(self, parent, transform)

  parent = property(Node.getParent, setParent)

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
    framework.base.mouseInterfaceNode.setMat(matrix)
    
    if rotate == False:
      camera.setEffect(panda.CompassEffect.make(self.world.scene))
