from morsel.platforms import *

#-------------------------------------------------------------------------------

def Actuator(**kargs):
  return framework.createInstance("actuators."+framework.world.physics,
    world = framework.world, **kargs)
