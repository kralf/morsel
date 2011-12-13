from morsel.morselc import Timestamp
from morsel.nodes import View, Text

#-------------------------------------------------------------------------------

class ClockView(View):
  def __init__(self, world, name, origin = [-1.05, 2], position = [-1, 1],
      period = 1.0, **kargs):
    View.__init__(self, world, name, **kargs)
    
    self.text = Text(world, name+"Text", text = "World time: n/a",
      origin = origin, position = position)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.text.text = "World time: %s" % Timestamp.toString(self.world.time)
  