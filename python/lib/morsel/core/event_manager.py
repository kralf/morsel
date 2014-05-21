from event_handler import EventHandler

from panda3d.direct.showbase.DirectObject import DirectObject

#-------------------------------------------------------------------------------

class EventManager(DirectObject):
  def __init__(self, **kargs):
    DirectObject.__init__(self)
    
    self.handlers = {}

#-------------------------------------------------------------------------------

  def addHandler(self, event, handler, priority = 0):
    if not isinstance(handler, EventHandler):
      handler = EventHandler(handler)
    
    if not self.handlers.has_key(event):
      self.handlers[event] = {}
      self.accept(event, self.dispatchEvent, [event])
    if not self.handlers[event].has_key(priority):
      self.handlers[event][priority] = []

    self.handlers[event][priority].append(handler)

#-------------------------------------------------------------------------------

  def addHandlers(self, handlers, priority = 0):
    for event, handler in handlers.items():
      self.addHandler(event, handler, priority)

#-------------------------------------------------------------------------------

  def removeHandler(self, event, handler, priority = 0):
    if self.handlers.has_key(event):
      if handler in self.handlers[event][priority]:
        self.handlers[event][priority].remove(handler)

        if not self.handlers[event][priority]:
          del self.handlers[event][priority]
        if not self.handlers[event]:
          del self.handlers[event]
          self.ignore(event)

        return
      
    framework.error("Bad handler for \""+event+"\" event.")

#-------------------------------------------------------------------------------

  def removeHandlers(self, handlers, priority = 0):
    for event, handler in handlers.items():
      self.removeHandler(event, handler, priority)

#-------------------------------------------------------------------------------

  def dispatchEvent(self, event):
    priority = sorted(self.handlers[event].keys())[-1]

    for handler in self.handlers[event][priority]:
      handler.call()
