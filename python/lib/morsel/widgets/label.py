from morsel.nodes import Widget

from panda3d.direct.gui.DirectGui import DirectLabel

#-------------------------------------------------------------------------------

class Label(Widget):
  def __init__(self, gui, name, text = None, align = None, **kargs):
    if not text:
      text = name
    self.alignments = {
      "Left": panda.TextNode.ALeft,
      "Center": panda.TextNode.ACenter,
      "Right": panda.TextNode.ARight
    }
    
    Widget.__init__(self, gui, name, widget = DirectLabel(scale = 0.05),
      text = text, **kargs)

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
