from morsel.gui import *

#-------------------------------------------------------------------------------

def GUI(**kargs):
  framework.gui = framework.createInstance("gui", type = "GUI", **kargs)
  return framework.gui
