from morsel.panda import *

#-------------------------------------------------------------------------------

class EventHandler(object):
  def __init__(self, function, *args, **kargs):
    super(EventHandler, self).__init__()

    self.function = function
    self.args = args
    self.kargs = kargs

#-------------------------------------------------------------------------------

  def call(self):
    self.function(*self.args, **self.kargs)
