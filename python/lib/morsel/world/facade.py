from morsel.core import *
from morsel.world import globals

#-------------------------------------------------------------------------------

def World(physics):
  if globals.world == None:
    globals.world = Instance("morsel.world."+physics, "World")
    return globals.world
  else:
    raise RuntimeError("World already initialized")
