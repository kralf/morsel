from panda3d.direct.showbase.DirectObject import DirectObject

#-------------------------------------------------------------------------------

class EventManager(DirectObject):
  def __init__(self):
    self.handlers = {}
    
#-------------------------------------------------------------------------------

  def addHandler(self, key, function):
    if not self.handlers.has_key(key):
      self.handlers[ key ] = {}
      
    self.handlers[key][function] = function
    self.accept(key, self.dispatch, [key])

#-------------------------------------------------------------------------------

  def dispatch(self, key):
    for function in self.handlers[key]:
      function(key)
