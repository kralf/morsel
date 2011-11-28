from morsel.panda import *
from node import Node

#-------------------------------------------------------------------------------

class Light(Node):
  def __init__(self, world, name, light, color = [1, 1, 1, 1], **kargs):
    self.light = light
    Node.__init__(self, world, name, color = color, **kargs)

    node = self.attachNewNode(self.light)
    self.world.scene.setLight(node)

#-------------------------------------------------------------------------------

  def setColor(self, color):
    Node.setColor(self, color)
    self.light.setColor(panda.Vec4(*color))

  color = property(Node.getColor, setColor)
