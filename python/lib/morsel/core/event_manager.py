from panda3d.direct.showbase.DirectObject import DirectObject

#-------------------------------------------------------------------------------

class EventManager(DirectObject):
  def __init__(self):
    DirectObject.__init__(self)

    self.eventHandlers = {}
    self.keyHandlers = {}

#-------------------------------------------------------------------------------

  def addEventHandler(self, event, function):
    if not self.eventHandlers.has_key(event):
      self.eventHandlers[event] = []

    self.eventHandlers[event].append(function)
    self.accept(event, self.dispatchEvent, [event])

#-------------------------------------------------------------------------------

  def addKeyHandler(self, key, function):
    if not self.keyHandlers.has_key(key):
      self.keyHandlers[key] = []
      
    self.keyHandlers[key].append(function)
    self.accept(key, self.dispatchKey, [key])

#-------------------------------------------------------------------------------

  def dispatchEvent(self, event):
    for function in self.eventHandlers[event]:
      function()

#-------------------------------------------------------------------------------

  def dispatchKey(self, key):
    for function in self.keyHandlers[key]:
      function()
