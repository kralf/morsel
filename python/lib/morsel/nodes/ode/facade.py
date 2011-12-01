from morsel.nodes.ode import *

#-------------------------------------------------------------------------------

def Body(**kargs):
  return framework.createInstance("nodes.ode.bodies",
    world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Geometry(**kargs):
  return framework.createInstance("nodes.ode.geometries",
    world = framework.world, **kargs)
