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
    
    Widget.__init__(self, gui, name, widget = DirectLabel(), text = text,
      **kargs)

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

  align = property(getAlign, setAlign)

#-------------------------------------------------------------------------------

  def setFrame(self, frame):
    Widget.setFrame(self, frame)
    frame = self.frame

    frame[2] = frame[2]+0.33*self.lineHeight
    frame[3] = frame[3]+0.33*self.lineHeight

    Widget.setFrame(self, frame)

  frame = property(Widget.getFrame, setFrame)

#-------------------------------------------------------------------------------

  def getLineHeight(self):
    if self.text:
      return 1.0/1.5*self.font.getLineHeight()
    else:
      return 0
    
  lineHeight = property(getLineHeight)
