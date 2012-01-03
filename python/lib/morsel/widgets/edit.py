from morsel.panda import *
from morsel.nodes import Widget

from panda3d.direct.gui.DirectGui import DirectEntry

#-------------------------------------------------------------------------------

class Edit(Widget):
  def __init__(self, gui, name, width = None, numLines = 1, focus = True,
      text = None, command = None, **kargs):
    Widget.__init__(self, gui, name, widget = DirectEntry(scale = 0.05),
      **kargs)

    if width:
      self.width = width
    self.numLines = numLines
    self.focus = focus
    if text:
      self.text = text
    if command:
      self.command = command

#-------------------------------------------------------------------------------

  def setWidth(self, width, node = None):
    text = self.text

    scale = self.widget.getScale()
    self.widget["width"] = width/scale[0]
    self.frame = [width, self.height]

    self.text = text

  width = property(Widget.getWidth, setWidth)

#-------------------------------------------------------------------------------

  def getText(self):
    return self.widget.get()

  def setText(self, text):
    self.widget.enterText(text)
    self.foregroundColor = self.foregroundColor

  text = property(getText, setText)

#-------------------------------------------------------------------------------

  def setForegroundColor(self, color):
    Widget.setForegroundColor(self, color)

    cursor = self.widget.guiItem.getCursorDef().getChild(0).node()
    writer = panda.GeomVertexWriter(cursor.modifyGeom(0).modifyVertexData(),
      "color")
    writer.setData4f(panda.Vec4(*color))
    writer.setData4f(panda.Vec4(*color))

  foregroundColor = property(Widget.getForegroundColor, setForegroundColor)

#-------------------------------------------------------------------------------

  def getNumLines(self):
    return self.widget["numLines"]

  def setNumLines(self, numLines):
    self.widget["numLines"] = numLines

  numLines = property(getNumLines, setNumLines)

#-------------------------------------------------------------------------------

  def getFocus(self):
    return self.widget["focus"]

  def setFocus(self, focus):
    self.widget["focus"] = focus
    self.foregroundColor = self.foregroundColor

  focus = property(getFocus, setFocus)

#-------------------------------------------------------------------------------

  def getCommand(self):
    return self.widget["command"]

  def setCommand(self, command):
    self.widget["command"] = command

  command = property(getCommand, setCommand)

#-------------------------------------------------------------------------------

  def getCursorPosition(self):
    return self.widget.guiItem.getCursorPosition()

  def setCursorPosition(self, position):
    self.widget.guiItem.setCursorPosition(position)

  cursorPosition = property(getCursorPosition, setCursorPosition)
