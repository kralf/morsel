from morsel.actors import *

#-------------------------------------------------------------------------------

def Actuator(**kargs):
  return framework.createInstance("actuators."+framework.world.physics,
    world = framework.world, **kargs)
