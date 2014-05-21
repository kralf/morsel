from morsel.world import *

#-------------------------------------------------------------------------------

def World(physics = None, **kargs):
  module = "world"
  if physics:
    module += "."+physics
  
  framework.world = framework.createInstance(module, type = "World", **kargs)
  
  return framework.world
