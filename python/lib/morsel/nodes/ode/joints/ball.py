from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.ode.joint import Joint

#-------------------------------------------------------------------------------

class Ball(Joint):
  def __init__(self, anchor = [0, 0, 0], **kargs):
    super(Ball, self).__init__(type = panda.OdeBallJoint, **kargs)
    
    self.anchor = anchor

#-------------------------------------------------------------------------------

  def getAnchor(self, node = None):
    if not node:
      node = self
      
    anchor = node.getRelativePoint(render, panda.Point3(
      self._joint.getAnchor()))
    
    return [anchor[0], anchor[1], anchor[2]]
  
  def setAnchor(self, anchor, node = None):
    if not node:
      node = self

    self._joint.setAnchor(render.getRelativePoint(node,
      panda.Point3(*anchor)))
  
  anchor = property(getAnchor, setAnchor)

#-------------------------------------------------------------------------------

  def getGlobalAnchor(self):
    return self.getAnchor(render)
  
  def setGlobalAnchor(self, anchor):
    self.setAnchor(anchor, render)
  
  globalAnchor = property(getGlobalAnchor, setGlobalAnchor)
  