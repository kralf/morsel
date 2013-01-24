from morsel.panda import *
from morsel.nodes import View
from morsel.morselc import LaserView as CLaserView

#-------------------------------------------------------------------------------

class LaserView(View):
  def __init__(self, world, name, sensor, shader = "laser_view.cg",
      color = [1, 0, 0, 0.5], showPoints = True, showLines = False,
      showColors = False, showLabels = False, useAlpha = True, **kargs):
    View.__init__(self, world, name, color = color, **kargs)

    self.sensor = sensor
    self.shaderProgram = ShaderProgram(filename = shader)
    self.showPoints = showPoints
    self.showLines = showLines
    self.showColors = showColors
    self.showLabels = showLabels
    self.useAlpha = useAlpha

    self.view = CLaserView(name, self.sensor.sensor, self.shaderProgram,
      panda.Vec4(*self.color), self.showPoints, self.showLines,
      self.showColors, self.showLabels, self.useAlpha)
    self.view.reparentTo(self.sensor)
    framework.addDrawCallback(name+"Callback", self.draw)

#-------------------------------------------------------------------------------

  def draw(self):
    self.view.update(self.world.time)
