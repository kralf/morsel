from morsel.panda import *
from morsel.nodes.ode.object import Object
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Solid(Geometry):
  def __init__(self, name = "Solid", geometry = None, placeable = True,
      **kargs):
    self._geometry = None
    self._mesh = None
    
    super(Solid, self).__init__(name = name, **kargs)
      
    self.hide(panda.BitMask32.allOn())
    
    self.placeable = placeable
    self.geometry = geometry
    
#-------------------------------------------------------------------------------

  def getObject(self):
    if isinstance(self.parent, Object):
      return self.parent
    else:
      return None

  def setObject(self, object):
    if self.parent != object:
      self.parent = object
    
    self.fit(object)
      
  object = property(getObject, setObject)

#-------------------------------------------------------------------------------

  def getGeometry(self):
    return self._geometry
    
  def setGeometry(self, geometry):
    self._geometry = geometry
    
    if self.object and self.object.collisionMasks:
      self._geometry.setCategoryBits(self.object.collisionMasks[0])
      self._geometry.setCollideBits(self.object.collisionMasks[1])
      
    if self._geometry and self.placeable:
      self._geometry.setPosition(*self.globalPosition)
      self._geometry.setQuaternion(self.globalQuaternion)
      
      if self.body:
        self._geometry.setBody(self.body._body)
        self._geometry.setOffsetPosition(*self.getPosition(self.body))
        self._geometry.setOffsetQuaternion(self.getQuaternion(self.body))
  
  geometry = property(getGeometry, setGeometry)

#-------------------------------------------------------------------------------

  def getBody(self):
    if self.object:
      return self.object.body
    else:
      return None
    
  body = property(getBody)
  
#-------------------------------------------------------------------------------

  def show(self, cameraMask = None):
    mesh = self.mesh
    
    if mesh:
      mesh.color = [1, 1, 1, 0.5]
      mesh.setTextureOff(1)
      mesh.setTransparency(panda.TransparencyAttrib.MAlpha)
    
    if cameraMask != None:
      Geometry.show(self, cameraMask)
    else:
      Geometry.show(self)

#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    if self._geometry and self.body and self.placeable:
      self._geometry.setOffsetPosition(*self.getPosition(self.body))
      
#-------------------------------------------------------------------------------

  def onRotate(self, rotation):
    if self._geometry and self.body and self.placeable:
      self._geometry.setOffsetQuaternion(self.getQuaternion(self.body))
    