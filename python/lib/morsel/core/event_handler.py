from morsel.panda import *

#-------------------------------------------------------------------------------

class EventHandler(object):
  def __init__(self, function, *args, **kargs):
    object.__init__(self)

    self.function = function
    self.args = args
    self.kargs = kargs

#-------------------------------------------------------------------------------

  def call(self):
    self.function(*self.args, **self.kargs)
