from morsel.nodes.panda import *

#-------------------------------------------------------------------------------

def Solid(type = None, **kargs):
  if not type:
    type = "Empty"
  
  return framework.createInstance("nodes.panda.solids", type = type, **kargs)
