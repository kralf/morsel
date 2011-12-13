from morsel.panda import *
from morsel.nodes import View, Text

#-------------------------------------------------------------------------------

class FramerateMeter(View):
  def __init__(self, world, name, origin = [1.1, 2], position = [1, 1],
      period = 1.0, **kargs):
    View.__init__(self, world, name, **kargs)
    
    self.text = Text(world, name+"Text", text = "Framerate: n/a",
      origin = origin, position = position)
    self.lastTime = -1.0
    self.period = period

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    if ((self.lastTime < 0) or (self.world.time-self.lastTime >= self.period)):
      self.text.text = ("Framerate: %.1f fps" %
        framework.scheduler.clock.getAverageFrameRate())
      self.lastTime = self.world.time
  