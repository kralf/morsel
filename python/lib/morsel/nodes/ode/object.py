from morsel.panda import *
from morsel.nodes.ode.facade import Joint
from morsel.nodes.object import Object as Base

#-------------------------------------------------------------------------------

class Object(Base):
  def __init__(self, solid = None, body = None, anchor = None,
      collisionMasks = None, **kargs):
    self._solid = None
    self._body = None
    self._anchorJoint = None
    self._joints = []
    self._collisionMasks = None
    
    super(Object, self).__init__(**kargs)
    
    self.solid = solid
    self.body = body
    self.anchor = anchor
    self.collisionMasks = collisionMasks
 
#-------------------------------------------------------------------------------

  def getSolid(self):
    return self._solid
    
  def setSolid(self, solid):
    if self._solid:
      self._solid.detachNode()
    
    self._solid = solid
    
    if self._solid:
      if self._solid.object != self:
        self._solid.object = self
  
  solid = property(getSolid, setSolid)
  
#-------------------------------------------------------------------------------

  def getBody(self):
    return self._body
    
  def setBody(self, body):
    if self._body:
      if self._anchorJoint:
        self._anchorJoint.detach()
      self._body.detachNode()
    
    self._body = body
    
    if self._body:
      if self._body.object != self:
        self._body.object = self
      if self.anchor and self.anchor.body:
        if not self._anchorJoint:
          self._anchorJoint = Joint(type = "Fixed")
        self._anchorJoint.attach(self.anchor, self)
  
  body = property(getBody, setBody)
  
#-------------------------------------------------------------------------------

  def setAnchor(self, anchor):
    if self._anchorJoint:
      self._anchorJoint.detach()
    
    Base.setAnchor(self, anchor)
    
    if self.anchor and self.body and self.anchor.body:
      if not self._anchorJoint:
        self._anchorJoint = Joint(type = "Fixed")
      self._anchorJoint.attach(self.anchor, self)
    
  anchor = property(Base.getAnchor, setAnchor)
  
#-------------------------------------------------------------------------------

  def getJoints(self):
    return self._joints
    
  joints = property(getJoints)
  
#-------------------------------------------------------------------------------

  def getCollisionMasks(self):
    return self._collisionMasks
    
  def setCollisionMasks(self, collisionMasks):
    self._collisionMasks = collisionMasks
    
    if self._collisionMasks and self.solid and self.solid.geometry:
      self.solid.geometry.setCategoryBits(self._collisionMasks[0])
      self.solid.geometry.setCollideBits(self._collisionMasks[1])

  collisionMasks = property(getCollisionMasks, setCollisionMasks)
  
#-------------------------------------------------------------------------------

  def findJoint(self, object = None):
    for joint in self.joints:
      objects = joint.objects      
      if (objects[0] == object) or (objects[1] == object):
        return joint
    
    return None
  
#-------------------------------------------------------------------------------

  def showSolids(self, cameraMask = 0x10000000):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      object.solid.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideSolids(self):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      object.solid.hide(panda.BitMask32.allOn())

#-------------------------------------------------------------------------------

  def showBodies(self, cameraMask = 0x10000000):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      object.body.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideBodies(self):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      object.body.hide(panda.BitMask32.allOn())

#-------------------------------------------------------------------------------

  def showJoints(self, cameraMask = 0x10000000):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      for joint in object.joints:
        joint.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideJoints(self):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      for joint in object.joints:
        joint.hide(panda.BitMask32.allOn())

#-------------------------------------------------------------------------------

  def applyBodyTransform(self):
    if self.solid and self.solid.geometry and self.solid.placeable:
      self.solid.geometry.setPosition(*self.solid.globalPosition)
      self.solid.geometry.setQuaternion(self.solid.globalQuaternion)
    if self.body:
      self.body._body.setPosition(*self.body.globalPosition)
      self.body._body.setQuaternion(self.body.globalQuaternion)

    for joint in self.joints:
      objects = joint.objects
      if (objects[0] == self) and objects[1]:
        objects[1].applyBodyTransform()
        
#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    self.applyBodyTransform()
    
#-------------------------------------------------------------------------------

  def onRotate(self, rotation):
    self.applyBodyTransform()
    