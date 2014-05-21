from morsel.panda import *
from morsel.nodes.widget import Widget

from panda3d.direct.gui.DirectGui import DirectLabel

#-------------------------------------------------------------------------------

class Label(Widget):
  def __init__(self, name = None, text = None, align = None, **kargs):
    if not text:
      if name:
        text = name
      else:
        text = self.__class__.__name__

    self.alignments = {
      "Left": panda.TextNode.ALeft,
      "Center": panda.TextNode.ACenter,
      "Right": panda.TextNode.ARight}
    
    super(Label, self).__init__(widget = DirectLabel(scale = 0.05), name = 
      name, text = text, **kargs)

    if align:
      self.align = align

#-------------------------------------------------------------------------------

  def getAlign(self):
    for align in self.alignments:
      if self.alignments[align] == self.widget["text_align"]:
        return align

    return None

  def setAlign(self, align):
    self.widget["text_align"] = self.alignments[align]
    self.updateBounds()

  align = property(getAlign, setAlign)
