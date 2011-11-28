from morsel.panda import *
from morsel.nodes import View
from morsel.morselc import LaserView as CLaserView

#-------------------------------------------------------------------------------

class LaserView(View):
  def __init__(self, world, name, sensor, color = [1, 0, 0, 0.5],
      showPoints = True, showLines = False, showColors = False,
      showLabels = False, **kargs):
    View.__init__(self, world, name, color = color, **kargs)

    self.sensor = sensor
    self.showPoints = showPoints
    self.showLines = showLines
    self.showColors = showColors
    self.showLabels = showLabels

    self.view = CLaserView(name, self.sensor.sensor, panda.Vec4(*self.color),
      self.showPoints, self.showLines, self.showColors, self.showLabels)
    self.view.reparentTo(self.sensor.mesh)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.view.update(self.world.time)
