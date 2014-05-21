from morsel.panda import *
from node import Node

#-------------------------------------------------------------------------------

class Widget(Node):
  def __init__(self, gui = None,  widget = None, anchor = None, origin =
      [0, 0], frame = None, margin = None, text = None, color = [0, 0, 0, 0.3],
      font = None, foregroundColor = [1, 1, 1, 1], backgroundColor = None,
      parent = None, scale = 1, **kargs):
    self.gui = gui

    if anchor and self.gui:
      parent = self.gui.anchors[anchor[0], anchor[1]]
    super(Widget, self).__init__(parent = parent, scale = scale, **kargs)

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
    self.font = font
    self.foregroundColor = foregroundColor
    self.backgroundColor = backgroundColor
    
    if self.gui:
      self.gui.registerWidget(self)
    
    self.updateBounds()

#-------------------------------------------------------------------------------

  def setParent(self, parent):
    if not parent:
      if self.gui:
        parent = self.gui.anchors["Center", "Center"]
      else:
        parent = render2d

    Node.setParent(self, parent)

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

  def getFrame(self, node = None):
    if self.widget:
      frame = self.widget["frameSize"]
      if frame:
        if not node:
          node = self
        topLeft = node.getRelativePoint(self.widget,
          panda.Point3(frame[0], 0, frame[3]))
        bottomRight = node.getRelativePoint(self.widget,
          panda.Point3(frame[1], 0, frame[2]))

        return [topLeft[0], bottomRight[0], bottomRight[2], topLeft[2]]

    return None

  def setFrame(self, frame, node = None):
    if self.widget:
      if len(frame) == 2:
        center = self.center
        frame = [center[0]-0.5*frame[0], center[0]+0.5*frame[0],
          center[1]-0.5*frame[1], center[1]+0.5*frame[1]]

      if not node:
        node = self
      topLeft = self.widget.getRelativePoint(node,
        panda.Point3(frame[0], 0, frame[3]))
      bottomRight = self.widget.getRelativePoint(node,
        panda.Point3(frame[1], 0, frame[2]))
      self.widget["frameSize"] = [topLeft[0], bottomRight[0],
        bottomRight[2], topLeft[2]]
      
      self.updateBounds()

  frame = property(getFrame, setFrame)

#-------------------------------------------------------------------------------

  def getMargin(self, node = None):
    if self.widget:
      margin = self.widget["pad"]
      if margin:
        if not node:
          node = self
        scale = self.widget.getScale(node)
        
        return [margin[0]*scale[0], margin[1]*scale[2]]

    return None

  def setMargin(self, margin, node = None):
    if self.widget:
      if not node:
        node = self
      scale = self.widget.getScale(node)
      
      self.widget["pad"] = [margin[0]/scale[0], margin[1]/scale[2]]
      
      self.updateBounds()

  margin = property(getMargin, setMargin)

#-------------------------------------------------------------------------------

  def getLeft(self, node = None):
    return self.getBounds(node)[0][0]

  left = property(getLeft)

#-------------------------------------------------------------------------------

  def getTop(self, node = None):
    return self.getBounds(node)[1][1]

  top = property(getTop)

#-------------------------------------------------------------------------------

  def getRight(self, node = None):
    return self.getBounds(node)[1][0]

  right = property(getRight)

#-------------------------------------------------------------------------------

  def getBottom(self, node = None):
    return self.getBounds(node)[0][1]

  bottom = property(getBottom)

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
    p_min, p_max = self.getBounds(node)
    return (p_min+p_max)*0.5

  center = property(getCenter)

#-------------------------------------------------------------------------------

  def getBounds(self, node = None):    
    if self.widget:
      bounds = self.widget.getBounds()

      p_min = panda.Point3(bounds[0], 0, bounds[2])
      p_max = panda.Point3(bounds[1], 0, bounds[3])
    else:
      p_min = panda.Point3(0, 0, 0)
      p_max = panda.Point3(0, 0, 0)

    if not node:
      node = self
    p_min = node.getRelativePoint(self.widget, p_min)
    p_max = node.getRelativePoint(self.widget, p_max)

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

  def getTextWidth(self, text, node = None):
    if not node:
      node = self      
    scale = self.widget.getScale(node)
    
    return self.font.getWidth(text)*scale[0]

#-------------------------------------------------------------------------------

  def getTextHeight(self, text, node = None):
    if not node:
      node = self
    scale = self.widget.getScale(node)

    return self.font.getHeight(text)*scale[2]

#-------------------------------------------------------------------------------

  def getFont(self):
    return self._font

  def setFont(self, font):
    if isinstance(font, str):
      font = Font(font)
    if font:
      self._font = font
    else:
      self._font = Font()
      
    self.widget["text_font"] = self._font.font
    self.updateBounds()

  font = property(getFont, setFont)

#-------------------------------------------------------------------------------

  def getColor(self):
    if self.hasColor():
      color = panda.NodePath.getColor(self)
      return [color[0], color[1], color[2], color[3]]
    else:
      return [0]*4

  def setColor(self, color):
    panda.NodePath.setColor(self, *color)
    
    if self.widget:
      self.widget["frameColor"] = self.color

  color = property(getColor, setColor)

#-------------------------------------------------------------------------------

  def getForegroundColor(self):
    return self._foregroundColor

  def setForegroundColor(self, color):
    if self.widget and color:
      self.widget["text_fg"] = color

    self._foregroundColor = color

  foregroundColor = property(getForegroundColor, setForegroundColor)

#-------------------------------------------------------------------------------

  def getBackgroundColor(self):
    return self._backgroundColor
      
  def setBackgroundColor(self, color):
    if self.widget and color:
      self.widget["text_bg"] = color

    self._backgroundColor = color

  backgroundColor = property(getBackgroundColor, setBackgroundColor)

#-------------------------------------------------------------------------------

  def updateBounds(self):
    if self.widget:
      center = self.center
      position = self.widget.getPos()

      self.widget.setPos(position[0]-0.5*self.width*self.origin[0]-center[0], 0,
        position[2]-0.5*self.height*self.origin[1]-center[1])

#-------------------------------------------------------------------------------

  def draw(self):
    pass
  