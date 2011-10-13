from morsel.core import *
from morsel.world import globals

import morsel.nodes
import inspect

#-------------------------------------------------------------------------------

def Mesh(name, filename = None, **kargs):
  if filename:
    meshFile = framework.findFile(filename)
    if not meshFile:
      raise RuntimeError("Mesh file '"+filename+"' not found")
  else:
    meshFile = None
    
  return morsel.nodes.Mesh(globals.world, name, filename = meshFile,
    **kargs)

#-------------------------------------------------------------------------------

def Collider(name, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics, "Collider",
    globals.world, name, *args, **kargs)

#-------------------------------------------------------------------------------

def Solid(name, type, mesh, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics+".solids", type,
    globals.world, name, mesh, *args, **kargs)

#-------------------------------------------------------------------------------

def Body(name, type, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics+".bodies", type,
    globals.world, name, *args, **kargs)

#-------------------------------------------------------------------------------

def Static(name, mesh, **kargs):
  return Instance("morsel.nodes", "Static", globals.world, name, mesh, **kargs)

#-------------------------------------------------------------------------------

def Scene(name, model = None, *args, **kargs):
  scene = Instance("morsel.nodes", "Scene", globals.world, name, *args,
    **kargs)
    
  if model:
    sceneFile = framework.findFile(model+".scm")
    if sceneFile:

      context = inspect.stack()[1][0].f_globals
      execfile(sceneFile, context)

      return scene
    else:
      raise RuntimeError("Scene file '"+model+".scm' not found")

#-------------------------------------------------------------------------------

def Actor(name, model, **kargs):
  actorFile = framework.findFile(model+".acm")
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

def Sensor(name, model, **kargs):
  sensorFile = framework.findFile(model+".sem")
  if sensorFile:
    context = {}
    parameters = kargs
    execfile(sensorFile, context, parameters)

    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.sensors."+globals.world.physics, type,
      globals.world, name, **parameters)
  else:
    raise RuntimeError("Sensor file '"+model+".sem' not found")

#-------------------------------------------------------------------------------

def Platform(name, model, **kargs):
  platformFile = framework.findFile(model+".pfm")
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

#-------------------------------------------------------------------------------

def View(name, type, *args, **kargs):
  return Instance("morsel.views", type, globals.world, name, *args, **kargs)

#-------------------------------------------------------------------------------

def Camera(position, object = None, **kargs):
  if object:
    object.attachCamera(position, **kargs)
  else:
    globals.world.scene.attachCamera(position, **kargs)
