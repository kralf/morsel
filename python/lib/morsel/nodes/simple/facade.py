from morsel.nodes.simple import *

#-------------------------------------------------------------------------------

def Geometry(**kargs):
  return framework.createInstance("nodes.simple.geometries",
    world = framework.world, **kargs)
