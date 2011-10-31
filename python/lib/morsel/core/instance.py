from morsel.panda import *

#-------------------------------------------------------------------------------

def Instance(moduleName, className, *args, **kargs):
  module = __import__(moduleName, globals(), locals(), [className])
  instance = getattr(module, className)

  return instance(*args, **kargs)
