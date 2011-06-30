import morsel.platforms
import morsel.platforms.globals as g
from morsel.core import *

#-------------------------------------------------------------------------------

def setPhysicsSimulation( value ):
  if g.world == None:
    g.simulation_type = value
  else:
    print "Cannot set simulation mode once the world is setup running"

#-------------------------------------------------------------------------------

def registerBody( name, mesh, terrain ):
  if g.world == None:
    g.world = Instance( "morsel.platforms." + g.simulation_type,
      "World", [], {} )
  return g.world.registerBody( name, mesh, terrain )


#-------------------------------------------------------------------------------

def Platform( name, platform_type, position = [0, 0, 0], orientation = [0, 0, 0]):
  if g.world == None:
    g.world = Instance( "morsel.platforms." + g.simulation_type,
      "World", [], {} )
  return g.world.addPlatform( name, platform_type, position, orientation )

