from morsel.panda import *
from object import Object

#-------------------------------------------------------------------------------

class Light(Object):
  def __init__(self, world, name, light, color = [1, 1, 1, 1], **kargs):
    self.light = light
    Object.__init__(self, world, name, color = color, **kargs)

    node = self.attachNewNode(self.light)
    self.world.scene.setLight(node)

#-------------------------------------------------------------------------------

  def setColor(self, color):
    Object.setColor(self, color)
    self.light.setColor(panda.Vec4(*color))

  color = property(Object.getColor, setColor)
