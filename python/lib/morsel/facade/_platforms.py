from morsel.world import globals
from morsel.core import *

#-------------------------------------------------------------------------------

def Platform( name, model, position = [0, 0, 0], orientation = [0, 0, 0],
           two_sided = False ):
  if globals.world != None:
    platform = globals.world.addPlatform( name, model )
    platform.setPos( *position )
    platform.setHpr( *orientation )
    platform.setTwoSided( two_sided )

    return platform
  else:
    raise RuntimeError( "World not initialized" )
