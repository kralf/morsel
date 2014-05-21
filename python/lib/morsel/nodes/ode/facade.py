from morsel.nodes.ode import *

#-------------------------------------------------------------------------------

def Solid(type = None, **kargs):
  if not type:
    type = "Empty"
  
  return framework.createInstance("nodes.ode.solids", type = type, **kargs)

#-------------------------------------------------------------------------------

def Body(type = None, **kargs):
  if not type:
    type = "Empty"
  
  return framework.createInstance("nodes.ode.bodies", type = type, **kargs)

#-------------------------------------------------------------------------------

def Joint(type = None, **kargs):
  if not type:
    type = "Fixed"
    
  return framework.createInstance("nodes.ode.joints", type = type, **kargs)
  