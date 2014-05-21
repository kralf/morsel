from morsel.panda import *
from solid import Solid
from morsel.nodes.iterator import Iterator
from morsel.nodes.scene import Scene as Base

#-------------------------------------------------------------------------------

class Scene(Base):
  def __init__(self, **kargs):
    super(Scene, self).__init__(**kargs)
      
    framework.addShortcut("alt-s", self.toggleShowSolids,
      "Show/hide collision solids in the scene")
  
#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

#-------------------------------------------------------------------------------

  def showSolids(self, cameraMask = 0x10000000):
    for object in self.objects:
      object.collider.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideSolids(self):
    for object in self.objects:
      object.collider.hide(panda.BitMask32.allOn())
      
#-------------------------------------------------------------------------------

  def toggleShowSolids(self):
    for object in self.objects:
      if not object.collider.isHidden(panda.BitMask32(0x10000000)):
        self.hideSolids()
        return
        
    self.showSolids()
    