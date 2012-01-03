from morsel.panda import *
from morsel.console import *
from morsel.widgets import Frame, Label, Edit
from morsel.console import Console as ConsoleBase
from morsel.core.event_handler import EventHandler

from panda3d.direct.gui.DirectGui import DirectFrame, DirectEntry, DirectLabel

from textwrap import TextWrapper

import sys, os, re, string

#-------------------------------------------------------------------------------

class Console(Frame):
  def __init__(self, gui, name = "Console", anchor = ["Center", "Bottom"],
      origin = [0, -1], frame = [2, 1.5],  helpColor = [0.8, 1.0, 0.8, 1.0],
      completeColor = [1.0, 0.8, 0.8, 1.0], outputLength = 1000,
      historyLength = 100, hidden = True, font = "monospace.bam", **kargs):
    self.console = None
    self.clipboard = Clipboard()
    
    self.handlers = {
      "page_up": EventHandler(self.scrollOutput, 5),
      "page_up-repeat": EventHandler(self.scrollOutput, 5),
      "page_down": EventHandler(self.scrollOutput, -5),
      "page_down-repeat": EventHandler(self.scrollOutput, -5),
      "arrow_up": EventHandler(self.scrollHistory, 1),
      "arrow_down": EventHandler(self.scrollHistory, -1),
      "control": EventHandler(self.unfocus),
      "control-up": EventHandler(self.focus),
      "control-c": EventHandler(self.copy),
      "control-x": EventHandler(self.cut),
      "control-v": EventHandler(self.paste),
      "tab": EventHandler(self.complete),
      "control-h": EventHandler(self.help)
    }

    framework.eventManager.addHandlers(self.handlers, 1)
    Frame.__init__(self, gui, name, anchor = anchor, origin = origin,
      frame = frame, hidden = hidden, font = Font(font), **kargs)

    self.helpColor = helpColor
    self.completeColor = completeColor
    self.outputLength = outputLength
    self.historyLength = historyLength

    self.label = Label(gui, name+"Label", parent = self, origin = [-1, -1],
      position = [self.left, self.bottom+0.017], text = "morsel>", font = font)
    self.input = Edit(gui, name+"Input", parent = self, origin = [-1, -1],
      position = [self.label.getRight(self)+0.01, self.bottom],
      width = self.right-self.label.getRight(self)-0.01,
      color = [0, 0, 0, 0], font = self.font, command = self.pushCommand)
    self.label.frame = [self.getLeft(self.label), self.getRight(self.label),
      self.input.getBottom(self.label), self.input.getTop(self.label)]

    self.outputs = []
    labelTop = self.top
    labelHeight = 0
    while labelTop-labelHeight > self.input.getTop(self):
      label = Label(gui, name+"Output", parent = self, origin = [-1, 1],
        position = [-1, labelTop], align = "Left", color = [0, 0, 0, 0],
        font = self.font)
      labelHeight = label.getHeight(self)
      labelTop = labelTop-labelHeight

      self.outputs.append(label)

    self.wrapper = TextWrapper()
    self.wrapper.width = int(self.width/self.outputs[0].getTextWidth("x"))

    self.history = [""]
    self.historyPosition = 0
    self.output = []
    self.outputPosition = 0

    self.write(framework.configuration.fullName)
    self.help()
  
#-------------------------------------------------------------------------------

  def setHidden(self, hidden):
    Frame.setHidden(self, hidden)
    
    if self.hidden:
      framework.eventManager.removeHandlers(self.handlers, 1)
    else:
      if not self.console:
        self.console = ConsoleBase(framework.locals)
      framework.eventManager.addHandlers(self.handlers, 1)
      self.focus()

  hidden = property(Frame.getHidden, setHidden)

#-------------------------------------------------------------------------------

  def write(self, output, prefix = None, color = None):
    if not prefix:
      prefix = ""
    if not color:
      color = self.foregroundColor
    
    if output:
      for line in output.split(os.linesep):
        line = re.sub(r"[^%s]" % re.escape(string.printable[:95]), "", line)
        line = "%s%s" % (prefix, line)

        for line in self.wrapper.wrap(line):
          self.output.insert(0, [line, color])
          if len(self.output) > self.outputLength:
            self.output.pop()

    self.updateOutput()

#-------------------------------------------------------------------------------

  def help(self, input = None):
    if not input:
      input = self.input.text
      
    if input:
      text = self.console.help(input)
      self.write(text, "?> ", self.helpColor)
    else:
      self.write("Use \"tab\" for completion, \"ctrl+h\" for contextual help",
        "?> ", self.helpColor)
      
#-------------------------------------------------------------------------------

  def complete(self, input = None):
    if not input:
      input = self.input.text
    
    if input:
      try:
        input, candidates = self.console.complete(input)
      except:
        pass
      else:
        self.input.text = input
        self.input.cursorPosition = len(input)

        if len(candidates) > 1:
          self.write("\n".join(candidates), "*> ", self.completeColor)
    
#-------------------------------------------------------------------------------

  def push(self, input):
    if input:
      self.write(input, "morsel> ")
      output = self.console.push(input)
      self.write(output, ">>> ")
  
#-------------------------------------------------------------------------------

  def focus(self):
    self.input.focus = True

#-------------------------------------------------------------------------------

  def unfocus(self):
    self.input.focus = False

#-------------------------------------------------------------------------------

  def copy(self):
    self.clipboard.text = self.input.text

#-------------------------------------------------------------------------------

  def paste(self):
    clipboardText = self.clipboard.text
    cursorPosition = self.input.cursorPosition

    if clipboardText:
      text = self.input.text
      lines = clipboardText.split(os.linesep)

      for i in range(len(lines)):
        line = re.sub(r"[^"+re.escape(string.printable[:95])+']', "", lines[i])

        if not i:
          line = text[0:cursorPosition]+line
        if i+1 < len(lines):
          self.input.text = line
          self.pushCommand(line)
        else:
          self.input.text = line+text[cursorPosition:]
          self.input.cursorPosition = len(line)

#-------------------------------------------------------------------------------

  def cut(self):
    self.clipboard.text = self.input.text
    self.input.text = ""

#-------------------------------------------------------------------------------

  def scrollOutput(self, numLines):
    self.outputPosition += numLines
    self.outputPosition = min(max(0, len(self.output)-len(self.outputs)),
      max(0, self.outputPosition))
      
    self.updateOutput()

#-------------------------------------------------------------------------------

  def scrollHistory(self, numCommands):
    historyPosition = self.historyPosition
    
    self.historyPosition += numCommands
    self.historyPosition = min(len(self.history)-1,
      max(0, self.historyPosition))
    self.history[historyPosition] = self.input.text
    command = self.history[self.historyPosition]
    
    self.input.text = command
    self.input.cursorPosition = len(command)

#-------------------------------------------------------------------------------

  def pushCommand(self, command):
    self.input.text = ""

    self.history.insert(1, command)
    if len(self.history) > self.historyLength:
      self.history.pop()
      
    self.history[0] = ""
    self.historyPosition = 0

    self.push(command)
    self.focus()

#-------------------------------------------------------------------------------

  def updateOutput(self):
    for i in range(len(self.outputs)):
      outputPosition = len(self.outputs)+self.outputPosition-i-1

      if outputPosition < len(self.output):
        line, color = self.output[outputPosition]

        self.outputs[i].text = line
        self.outputs[i].foregroundColor = color
      else:
        self.outputs[i].text = ""
