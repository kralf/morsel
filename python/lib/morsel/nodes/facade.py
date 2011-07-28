from morsel.core import *
from morsel.world import globals

import morsel.nodes

#-------------------------------------------------------------------------------

def Mesh(name, filename, **kargs):
  meshFile = findFile(filename)
  if meshFile:
    return morsel.nodes.Mesh(globals.world, name, filename = meshFile, **kargs)
  else:
    raise RuntimeError("Mesh file '"+filename+"' not found")

#-------------------------------------------------------------------------------

def Collider(name, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics, "Collider",
    globals.world, name, *args, **kargs)

#-------------------------------------------------------------------------------

def Solid(name, type, mesh, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics+".solids", type,
    globals.world, name, mesh, *args, **kargs)

#-------------------------------------------------------------------------------

def Body(name, type, solid, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics+".bodies", type,
    globals.world, name, solid, *args, **kargs)

#-------------------------------------------------------------------------------

def Environment(name, mesh, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics, "Environment",
    globals.world, name, mesh, *args, **kargs)

#-------------------------------------------------------------------------------

def Actor(name, model, **kargs):
  actorFile = findFile(model+".acm")
  if actorFile:
    context = {}
    parameters = kargs
    execfile(actorFile, context, parameters)

    type = parameters["type"]
    del parameters["type"]
    
    return Instance("morsel.actors."+globals.world.physics, type,
      globals.world, name, **parameters)
  else:
    raise RuntimeError("Actor file '"+model+".acm' not found")

#-------------------------------------------------------------------------------

def Platform(name, model, **kargs):
  platformFile = findFile(model+".pfm")
  if platformFile:
    context = {}
    parameters = kargs
    execfile(platformFile, context, parameters)
    
    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.platforms."+globals.world.physics, type,
      globals.world, name, **parameters)
  else:
    raise RuntimeError("Platform file '"+model+".pfm' not found")
