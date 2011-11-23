from morsel.core import Instance
from morsel.world import globals

#-------------------------------------------------------------------------------

def Body(name, type, *args, **kargs):
  return Instance("morsel.nodes.ode.bodies", type, globals.world, name,
    *args, **kargs)

#-------------------------------------------------------------------------------

def Geometry(name, type, *args, **kargs):
  return Instance("morsel.nodes.ode.geometries", type, globals.world, name,
    *args, **kargs)
