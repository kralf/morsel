from morsel.panda import *
from morsel.nodes.widget import Widget

from panda3d.direct.gui.DirectGui import DirectFrame

#-------------------------------------------------------------------------------

class Frame(Widget):
  def __init__(self, **kargs):
    super(Frame, self).__init__(widget = DirectFrame(), **kargs)

#-------------------------------------------------------------------------------

  def getBounds(self, node = None):
    if self.frame:
      bounds = self.getFrame(node)

      return (panda.Point2(bounds[0], bounds[2]),
        panda.Point2(bounds[1], bounds[3]))
    else:
      return Widget.getBounds(self, node)

  bounds = property(getBounds)
