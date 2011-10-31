from morsel.core import Instance
from morsel.world import globals

#-------------------------------------------------------------------------------

def World(physics, *args, **kargs):
  if globals.world == None:
    globals.world = Instance("morsel.world."+physics, "World", *args, **kargs)
    return globals.world
  else:
    framework.error("World already initialized")
