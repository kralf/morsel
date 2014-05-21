from morsel.panda import *

from panda3d.direct.gui.DirectGui import DGG

#-------------------------------------------------------------------------------

class Font(object):
  def __init__(self, filename = None, **kargs):
    self.filename = None
    self.model = None

    super(Font, self).__init__()
    
    if filename:
      self.filename = filename
      self.model = loader.loadModel(self.filename)
      self.font = panda.StaticTextFont(self.model.node())
    else:
      self.font = DGG.getDefaultFont()

    self.metrics = panda.TextNode("FontMetrics")
    self.metrics.setFont(self.font)

#-------------------------------------------------------------------------------

  def getWidth(self, text):
    self.metrics.setText(text)
    return self.metrics.getWidth()

#-------------------------------------------------------------------------------

  def getHeight(self, text):
    self.metrics.setText(text)
    return self.metrics.getHeight()
    