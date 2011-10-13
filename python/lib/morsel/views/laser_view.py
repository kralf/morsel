from morsel.nodes import View
from morsel.morselc import LaserView as CLaserView

#-------------------------------------------------------------------------------

class LaserView(View):
  def __init__(self, world, name, sensor, color = [1, 0, 0, 0.5],
      showPoints = True, showLines = False, showColors = False, **kargs):
    View.__init__(self, world, name, **kargs)

    self.sensor = sensor
    self.color = color
    self.showPoints = showPoints
    self.showLines = showLines
    self.showColors = showColors

    self.view = CLaserView(name, self.sensor.sensor, self.color[0],
      self.color[1], self.color[2], self.color[3], self.showPoints,
      self.showLines, self.showColors)
    self.view.reparentTo(self.sensor.mesh)

#-------------------------------------------------------------------------------

  def update(self):
    self.view.update(self.world.time)
