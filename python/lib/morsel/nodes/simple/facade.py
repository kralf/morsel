from morsel.core import Instance
from morsel.world import globals

#-------------------------------------------------------------------------------

def Geometry(name, type, *args, **kargs):
  return Instance("morsel.nodes.simple.geometries", type, globals.world, name,
    *args, **kargs)
