from morsel.panda import *
from node import Node

#-------------------------------------------------------------------------------

class Light(Node):
  def __init__(self, world = None, light = None, color = [1, 1, 1, 1],
      **kargs):
    self.world = world
    self._light = None
    
    super(Light, self).__init__(**kargs)

    self.light = light
    self.color = color

#-------------------------------------------------------------------------------

  def setParent(self, parent):
    if not parent and self.world:
      parent = self.world.scene

    Node.setParent(self, parent)

  parent = property(Node.getParent, setParent)
  
#-------------------------------------------------------------------------------

  def getLight(self):
    return self._light

  def setLight(self, light):
    self._light = light
    
    if self._light:
      self._light.setColor(panda.Vec4(*self.color))
      node = self.attachNewNode(self._light)
      if self.world:
        self.world.scene.setLight(node)

  light = property(getLight, setLight)
  
#-------------------------------------------------------------------------------

  def getColor(self):
    if self.hasColor():
      color = panda.NodePath.getColor(self)
      return [color[0], color[1], color[2], color[3]]
    else:
      return [0]*4

  def setColor(self, color):
    panda.NodePath.setColor(self, *color)
    
    if self.light:
      self.light.setColor(panda.Vec4(*color))

  color = property(getColor, setColor)
