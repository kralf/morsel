from morsel.panda import *
from solid import Solid
from body import Body
from joint import Joint
from morsel.nodes.iterator import Iterator
from morsel.nodes.scene import Scene as Base

#-------------------------------------------------------------------------------

class Scene(Base):
  def __init__(self, **kargs):
    super(Scene, self).__init__(**kargs)
      
    framework.addShortcut("alt-s", self.toggleShowSolids,
      "Show/hide collision solids in the scene")
    framework.addShortcut("alt-b", self.toggleShowBodies,
      "Show/hide rigid bodies in the scene")
    framework.addShortcut("alt-j", self.toggleShowJoints,
      "Show/hide rigid body joints in the scene")
  
#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

#-------------------------------------------------------------------------------

  def getBodies(self):
    return Iterator(self, Body).generator

  bodies = property(getBodies)

#-------------------------------------------------------------------------------

  def getJoints(self):
    return Iterator(self, Joint).generator

  joints = property(getJoints)

#-------------------------------------------------------------------------------

  def showSolids(self, cameraMask = 0x10000000):
    for solid in self.solids:
      solid.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideSolids(self):
    for solid in self.solids:
      solid.hide(panda.BitMask32.allOn())
      
#-------------------------------------------------------------------------------

  def showBodies(self, cameraMask = 0x10000000):
    for body in self.bodies:
      body.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideBodies(self):
    for body in self.bodies:
      body.hide(panda.BitMask32.allOn())
      
#-------------------------------------------------------------------------------

  def showJoints(self, cameraMask = 0x10000000):
    for joint in self.joints:
      joint.show(panda.BitMask32(cameraMask))

#-------------------------------------------------------------------------------

  def hideJoints(self):
    for joint in self.joints:
      joint.hide(panda.BitMask32.allOn())
      
#-------------------------------------------------------------------------------

  def toggleShowSolids(self):
    for solid in self.solids:
      if not solid.isHidden(panda.BitMask32(0x10000000)):
        self.hideSolids()
        return
        
    self.showSolids()

#-------------------------------------------------------------------------------

  def toggleShowBodies(self):
    for body in self.bodies:
      if not body.isHidden(panda.BitMask32(0x10000000)):
        self.hideBodies()
        return
        
    self.showBodies()
    
#-------------------------------------------------------------------------------

  def toggleShowJoints(self):
    for joint in self.joints:
      if not joint.isHidden(panda.BitMask32(0x10000000)):
        self.hideJoints()
        return
        
    self.showJoints()
    