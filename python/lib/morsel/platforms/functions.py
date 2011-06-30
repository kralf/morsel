from morsel.core import *

#-------------------------------------------------------------------------------

def loadPlatform( simulation_type, platform_type, parameters, position, orientation ):
  context = {}
  configFile = findFile( platform_type + ".pfm" )
  if configFile:
    execfile( configFile, context )
    platform = Instance( "morsel.platforms." + simulation_type, context["type"],
      parameters, context["arguments"] )
    platform.reparentTo( render )
    platform.setPos( panda.VBase3( *position ) )
    platform.setHpr( panda.VBase3( *orientation ) )
    return platform
  else:
    error ( "Configuration file '" + platform + ".pfm' does not exist." ) 
