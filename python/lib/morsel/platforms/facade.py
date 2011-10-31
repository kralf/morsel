from morsel.core import *
from morsel.world import globals

#-------------------------------------------------------------------------------

def Actuator(name, type, *args, **kargs):
  return Instance("morsel.actuators."+globals.world.physics, type,
    globals.world, name, *args, **kargs)
