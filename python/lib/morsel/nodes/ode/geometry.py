from morsel.panda import *
from morsel.nodes import Object

#-------------------------------------------------------------------------------

class Geometry(Object):
  def __init__(self, world, name, solid, geometry = None, placeable = True,
      **kargs):
    self.geometry = geometry
    self.body = None
    self.positionOffset = [0, 0, 0]
    self.orientationOffset = [0, 0, 0]
    self.placeable = placeable
    
    Object.__init__(self, world, name, **kargs)

    self.solid = solid

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None):
    Object.setPosition(self, position, node)
    
    if self.geometry:
      self.geometry.setPosition(self.getPos(self.world.scene))

  position = property(Object.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Object.setOrientation(self, orientation, node)
    
    if self.geometry:
      self.geometry.setQuaternion(self.getQuat(self.world.scene))

  orientation = property(Object.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getPositionOffset(self):
    return self._positionOffset

  def setPositionOffset(self, positionOffset):
    self._positionOffset = positionOffset
    if self.geometry and self.body:
      self.geometry.setOffsetPosition(*self._positionOffset)

  positionOffset = property(getPositionOffset, setPositionOffset)

#-------------------------------------------------------------------------------

  def getOrientationOffset(self):
    return self._orientationOffset

  def setOrientationOffset(self, orientationOffset):
    self._orientationOffset = orientationOffset
    if self.geometry and self.body:
      quaternion = panda.Quat()
      quaternion.setHpr(panda.Vec3(*self._orientationOffset))
      
      self.geometry.setOffsetQuaternion(quaternion)

  orientationOffset = property(getOrientationOffset, setOrientationOffset)

#-------------------------------------------------------------------------------

  def getGeometry(self):
    if hasattr(self, "_geometry"):
      return self._geometry
    else:
      return None

  def setGeometry(self, geometry):
    self._geometry = geometry
    if self._geometry and self.body:
      self._geometry.setBody(self.body.body)

      positionOffset = (panda.Vec3(*self.globalPosition)-
        panda.Vec3(*self.body.globalPosition))
      orientationOffset = (panda.Vec3(*self.globalOrientation)-
        panda.Vec3(*self.body.globalOrientation))

      self.positionOffset = [positionOffset[0], positionOffset[1],
        positionOffset[2]]
      self.orientationOffset = [orientationOffset[0], orientationOffset[1],
        orientationOffset[2]]

    if self._geometry and framework.debug:
      self.display = self.makeDisplay()
      if self.display:
        self.display.parent = self
        self.display.color = [1, 1, 1, 0.5]
        self.display.setTextureOff(1)
        self.display.setTransparency(panda.TransparencyAttrib.MAlpha)

    if self._geometry:
      self.updateTransform()

  geometry = property(getGeometry, setGeometry)

#-------------------------------------------------------------------------------

  def getBody(self):
    if hasattr(self, "_body"):
      return self._body
    else:
      return None

  def setBody(self, body):
    self._body = body
    if self.geometry and self._body:
      self.geometry.setBody(self._body.body)
      
      positionOffset = (panda.Vec3(*self.globalPosition)-
        panda.Vec3(*self._body.globalPosition))
      orientationOffset = (panda.Vec3(*self.globalOrientation)-
        panda.Vec3(*self._body.globalOrientation))
        
      self.positionOffset = [positionOffset[0], positionOffset[1],
        positionOffset[2]]
      self.orientationOffset = [orientationOffset[0], orientationOffset[1],
        orientationOffset[2]]

  body = property(getBody, setBody)

#-------------------------------------------------------------------------------

  def getCollisionMasks(self):
    if self.geometry:
      return [self.geometry.getCategoryBits(), self.geometry.getCollideBits()]
    else:
      return None

  def setCollisionMasks(self, collisionMasks):
    if self.geometry:
      self.geometry.setCategoryBits(collisionMasks[0])
      self.geometry.setCollideBits(collisionMasks[1])

  collisionMasks = property(getCollisionMasks, setCollisionMasks)


#-------------------------------------------------------------------------------

  def updateTransform(self):
    if self.geometry and self.placeable:
      self.geometry.setPosition(self.getPos(self.world.scene))
      self.geometry.setQuaternion(self.getQuat(self.world.scene))

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return None
