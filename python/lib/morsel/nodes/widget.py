from morsel.panda import *
from node import Node

#-------------------------------------------------------------------------------

class Widget(Node):
  def __init__(self, gui, name, widget = None, anchor = None, origin = [0, 0],
      frame = None, margin = None, text = None, color = [0, 0, 0, 0.3],
      font = None, foregroundColor = [1, 1, 1, 1], backgroundColor = None,
      parent = None, scale = 0.05, **kargs):
    self.gui = gui

    if anchor:
      parent = gui.anchors[anchor[0], anchor[1]]
    Node.__init__(self, name, parent = parent, scale = scale, **kargs)

    self.widget = widget
    self.origin = origin
    if text:
      self.text = text
    if frame:
      self.frame = frame
    if margin:
      self.margin = margin
    if color:
      self.color = color
    if font:
      self.font = font
    if foregroundColor:
      self.foregroundColor = foregroundColor
    if backgroundColor:
      self.backgroundColor = backgroundColor
    
    self.gui.registerWidget(self)

#-------------------------------------------------------------------------------

  def setParent(self, parent, transform = False):
    if not parent:
      parent = self.gui.anchors["Center", "Center"]

    Node.setParent(self, parent, transform)

  parent = property(Node.getParent, setParent)

#-------------------------------------------------------------------------------

  def getPosition(self, node = None):
    position = Node.getPosition(self, node)
    return [position[0], position[2]]

  def setPosition(self, position, node = None):
    Node.setPosition(self, [position[0], 0, position[1]], node)

  position = property(getPosition, setPosition)

#-------------------------------------------------------------------------------

  def getOrientation(self, node = None):
    orientation = Node.getOrientation(self, node)
    return orientation[0]

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, [orientation, 0, 0], node)

  orientation = property(getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def getScale(self, node = None):
    scale = Node.getScale(self, node)
    return [scale[0], scale[2]]

  def setScale(self, scale, node = None):
    if isinstance(scale, list):
      scale = [scale[0], 1, scale[1]]
    Node.setScale(self, scale, node)

  scale = property(getScale, setScale)

#-------------------------------------------------------------------------------

  def getWidget(self):
    return self._widget

  def setWidget(self, widget):
    self._widget = widget

    if self._widget:
      self._widget.reparentTo(self)

  widget = property(getWidget, setWidget)

#-------------------------------------------------------------------------------

  def getOrigin(self):
    return self._origin

  def setOrigin(self, origin):
    self._origin = origin
    self.updateBounds()

  origin = property(getOrigin, setOrigin)

#-------------------------------------------------------------------------------

  def getFrame(self):
    if self.widget:
      return self.widget["frameSize"]
    else:
      return None

  def setFrame(self, frame):
    if self.widget:
      if len(frame) == 2:
        frame = [-0.5*frame[0], 0.5*frame[0], -0.5*frame[1], 0.5*frame[1]]
      self.widget["frameSize"] = frame
      self.updateBounds()

  frame = property(getFrame, setFrame)

#-------------------------------------------------------------------------------

  def getMargin(self):
    if self.widget:
      return self.widget["pad"]
    else:
      return None

  def setMargin(self, margin):
    if self.widget:
      self.widget["pad"] = margin
      self.updateBounds()

  margin = property(getMargin, setMargin)

#-------------------------------------------------------------------------------

  def getWidth(self, node = None):
    p_min, p_max = self.getBounds(node)
    return p_max[0]-p_min[0]

  width = property(getWidth)

#-------------------------------------------------------------------------------

  def getHeight(self, node = None):
    p_min, p_max = self.getBounds(node)
    return p_max[1]-p_min[1]

  height = property(getHeight)

#-------------------------------------------------------------------------------

  def getCenter(self, node = None):
    if self.widget:
      center = self.widget.getCenter()
      p_center = panda.Point3(center[0], 0, center[1])
    else:
      p_center = panda.Point3(*self.position)

    if not node:
      node = self
    p_center = node.getRelativePoint(self, p_center)

    return panda.Point2(p_center[0], p_center[2])

  center = property(getCenter)

#-------------------------------------------------------------------------------

  def getBounds(self, node = None):    
    if self.widget:
      bounds = self.widget.getBounds()

      p_min = panda.Point3(bounds[0], 0, bounds[2])
      p_max = panda.Point3(bounds[1], 0, bounds[3])
    else:
      p_min = panda.Point3(*self.position)
      p_max = panda.Point3(*self.position)

    if not node:
      node = self
    p_min = node.getRelativePoint(self, p_min)
    p_max = node.getRelativePoint(self, p_max)

    return (panda.Point2(p_min[0], p_min[2]), panda.Point2(p_max[0], p_max[2]))

  bounds = property(getBounds)

#-------------------------------------------------------------------------------

  def getText(self):
    return self.widget["text"]

  def setText(self, text):
    self.widget["text"] = text
    self.margin = self.margin
    
    self.updateBounds()

  text = property(getText, setText)

#-------------------------------------------------------------------------------

  def getFont(self):
    return self.widget["text_font"]

  def setFont(self, font):
    self.widget["text_font"] = font
    self.updateBounds()

  font = property(getFont, setFont)

#-------------------------------------------------------------------------------

  def setColor(self, color):
    Node.setColor(self, color)
    
    if self.widget:
      self.widget["frameColor"] = self.color

  color = property(Node.getColor, setColor)

#-------------------------------------------------------------------------------

  def getForegroundColor(self):
    if self.widget:
      return self.widget["text_fg"]
    else:
      return None

  def setForegroundColor(self, color):
    if self.widget:
      self.widget["text_fg"] = color

  foregroundColor = property(getForegroundColor, setForegroundColor)

#-------------------------------------------------------------------------------

  def getBackgroundColor(self):
    if self.widget:
      return self.widget["text_bg"]
    else:
      return None
      
  def setBackgroundColor(self, color):
    if self.widget:
      self.widget["text_bg"] = color

  backgroundColor = property(getBackgroundColor, setBackgroundColor)

#-------------------------------------------------------------------------------

  def updateBounds(self):
    if self.widget:
      center = self.center
      self.widget.setPos(-0.5*self.width*self.origin[0]-center[0], 0,
        -0.5*self.height*self.origin[1]-center[1])

#-------------------------------------------------------------------------------

  def update(self):
    pass
  