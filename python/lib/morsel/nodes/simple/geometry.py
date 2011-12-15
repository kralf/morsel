from morsel.panda import *
from morsel.nodes import Object

#-------------------------------------------------------------------------------

class Geometry(Object):
  def __init__(self, world, name, solid, geometry = None, **kargs):
    self.solid = solid
    self.geometry = geometry

    Object.__init__(self, world, name, **kargs)

    if framework.debug:
      self.display = self.makeDisplay()
      if self.display:
        self.display.parent = self
        self.display.color = [1, 1, 1, 0.5]
        self.display.setTransparency(panda.TransparencyAttrib.MAlpha)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    return None
    