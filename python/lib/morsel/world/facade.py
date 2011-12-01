from morsel.world import *

#-------------------------------------------------------------------------------

def World(physics, **kargs):
  framework.world = framework.createInstance("world."+physics,
    type = "World", **kargs)
  return framework.world
