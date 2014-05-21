from morsel.panda import *
from morsel.nodes.view import View
from morsel.morselc import LaserView as CLaserView

#-------------------------------------------------------------------------------

class LaserView(View):
  def __init__(self, sensor = None, shader = "laser_view.cg", color = 
      [1, 0, 0, 0.5], showPoints = True, showLines = False, showColors = 
      False, showLabels = False, useAlpha = True, cameraMask = 0x00000010,
      **kargs):
    self._sensor = None
    self.view = None
    
    super(LaserView, self).__init__(color = color, **kargs)

    self.shaderProgram = ShaderProgram(filename = shader)
    self.showPoints = showPoints
    self.showLines = showLines
    self.showColors = showColors
    self.showLabels = showLabels
    self.useAlpha = useAlpha
    self.cameraMask = cameraMask
    self.sensor = sensor

    self.hide(panda.BitMask32.allOn())
    self.show(panda.BitMask32(self.cameraMask))
    
    framework.addDrawCallback(self.name+" <Callback>", self.draw)

#-------------------------------------------------------------------------------

  def getSensor(self):
    return self._sensor
    
  def setSensor(self, sensor):
    if self._sensor:
      self.view.detachNode()
      self.view = None
      self.detachNode()
      
    self._sensor = sensor
    
    if self._sensor:
      self.view = CLaserView("CLaserView", self.sensor.sensor,
        self.shaderProgram, panda.Vec4(*self.color), self.showPoints,
        self.showLines, self.showColors, self.showLabels, self.useAlpha)
      self.view.reparentTo(self)
      self.parent = self._sensor
      
  sensor = property(getSensor, setSensor)

#-------------------------------------------------------------------------------

  def draw(self):
    if self.view and self.world:
      self.view.update(self.world.time)
