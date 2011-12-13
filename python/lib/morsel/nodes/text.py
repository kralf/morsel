from morsel.panda import *
from node import Node

#-------------------------------------------------------------------------------

class Text(Node):
  def __init__(self, world, name, text = "", origin = [0, 0],
      backgroundColor = [0, 0, 0, 0.33], margin = [0.5, 0.5, 0.1, 0.1],
      position = [0, 0], scale = 0.05, **kargs):
    self.node = panda.TextNode(name+"Node")
    self.node.setCardDecal(True)
    self.origin = origin
    
    Node.__init__(self, world, name, position = position, scale = scale,
      **kargs)

    self.attachNewNode(self.node)
    self.text = text
    
    if backgroundColor:
      self.backgroundColor = backgroundColor
    if margin:
      self.margin = margin

    framework.eventManager.addEventHandler("aspectRatioChanged", self.update)

#-------------------------------------------------------------------------------

  def setParent(self, parent, transform = False):
    if not parent:
      parent = aspect2d

    Node.setParent(self, parent, transform)

  parent = property(Node.getParent, setParent)

#-------------------------------------------------------------------------------

  def getPosition(self, node = None):
    return self._position

  def setPosition(self, position, node = None):
    self._position = position
    
    properties = framework.base.win.getProperties()
    ratio = properties.getXSize()/float(properties.getYSize())
    extensions = self.extensions
    offset =  [0.5*extensions[0]*(-self.origin[0]-1),
      0.5*extensions[1]*(-self.origin[1]+1)-self.lineHeight]

    if ratio > 1:
      Node.setPosition(self, [position[0]*ratio+offset[0], 0,
        position[1]+offset[1]], node)
    else:
      Node.setPosition(self, [position[0]+offset[0], 0,
        position[1]/ratio+offset[1]], node)

  position = property(getPosition, setPosition)

#-------------------------------------------------------------------------------

  def getScale(self, node = None):
    scale = Node.getScale(self, node)
    return [scale[0], scale[2]]

  def setScale(self, scale, node = None):
    if isinstance(scale, list):
      scale = [scale[0], 1, scale[1]]
    Node.setScale(self, scale, node)

    self.update()

  scale = property(getScale, setScale)

#-------------------------------------------------------------------------------

  def getOrigin(self):
    return self._origin

  def setOrigin(self, origin):
    self._origin = origin
    self.update()

  origin = property(getOrigin, setOrigin)

#-------------------------------------------------------------------------------

  def getText(self):
    return self.node.getText()

  def setText(self, text):
    self.node.setText(text)
    self.update()

  text = property(getText, setText)

#-------------------------------------------------------------------------------

  def getBackgroundColor(self):
    color = self.node.getCardColor()
    return [color[0], color[1], color[2], color[3]]

  def setBackgroundColor(self, color):
    self.node.setCardColor(*color)

  backgroundColor = property(getBackgroundColor, setBackgroundColor)

#-------------------------------------------------------------------------------

  def getMargin(self):
    margin = self.node.getCardAsSet()
    return [margin[0], margin[1], margin[2], margin[3]]

  def setMargin(self, margin):
    self.node.setCardAsMargin(*margin)

  margin = property(getMargin, setMargin)

#-------------------------------------------------------------------------------

  def getExtensions(self):
    return [self.node.getWidth()*self.scale[0],
      self.node.getHeight()*self.scale[1]]

  extensions = property(getExtensions)

#-------------------------------------------------------------------------------

  def getLineHeight(self):
    return 1.0/1.5*self.node.getLineHeight()*self.scale[1]
    
  lineHeight = property(getLineHeight)

#-------------------------------------------------------------------------------

  def update(self):
    if self.text:
      self.position = self.position
