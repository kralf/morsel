from morsel.panda import *
from morsel.nodes.object import Object as Base

#-------------------------------------------------------------------------------

class Object(Base):
  def __init__(self, solid = None, collisionMasks = None, **kargs):
    self.collider = None
    self._solid = None
    
    super(Object, self).__init__(**kargs)
    
    node = panda.CollisionNode("Collider")
    self.collider = self.attachNewNode(node)
    self.collider.show()
    self.collider.hide(panda.BitMask32.allOn())
      
    self.solid = solid
    self.collisionMasks = collisionMasks
    
    if self.world:
      self.world.addCollider(self.collider, self)
 
#-------------------------------------------------------------------------------

  def getSolid(self):
    return self._solid
    
  def setSolid(self, solid):
    if self._solid:
      self.collider.node().clearSolids()
      self._solid.detachNode()
    
    self._solid = solid
    
    if self._solid:
      if self._solid.object != self:
        self._solid.object = self
      if self._solid.geometry:
        self.collider.node().addSolid(self._solid.geometry)
  
  solid = property(getSolid, setSolid)
  
#-------------------------------------------------------------------------------

  def getCollisionMasks(self):
    if self.collider:
      return [self.collider.node().getFromCollideMask().getWord(),
        self.collider.node().getIntoCollideMask().getWord()]
    else:
      return None
    
  def setCollisionMasks(self, collisionMasks):
    if collisionMasks:
      self.collider.node().setFromCollideMask(
        panda.BitMask32(collisionMasks[0]))
      self.collider.node().setIntoCollideMask(
        panda.BitMask32(collisionMasks[1]))

  collisionMasks = property(getCollisionMasks, setCollisionMasks)

#-------------------------------------------------------------------------------

  def showSolids(self, cameraMask = 0x10000000):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      object.collider.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideSolids(self):
    objects = Iterator(self, Object).generator
    
    for object in objects:
      object.collider.hide(panda.BitMask32.allOn())
    