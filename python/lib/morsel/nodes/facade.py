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

def Path(name, filename = None, **kargs):
  if filename:
    pathFile = framework.findFile(filename)
    if not pathFile:
      raise RuntimeError("Path file '"+filename+"' not found")
  else:
    pathFile = None

  return morsel.nodes.Path(globals.world, name, filename = pathFile,
    **kargs)

#-------------------------------------------------------------------------------

def Collider(name, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics, "Collider",
    globals.world, name, *args, **kargs)

#-------------------------------------------------------------------------------

def Solid(name, type, *args, **kargs):
  return Instance("morsel.nodes."+globals.world.physics+".solids", type,
    globals.world, name, *args, **kargs)

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

def Actuator(name, model = None, *args, **kargs):
  actorFile = framework.findFile(model+".acm")
  if actorFile:
    context = {}
    parameters = {}
    execfile(actorFile, context, parameters)
    parameters.update(kargs)

    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.actuators."+globals.world.physics, type,
      globals.world, name, **parameters)
  else:
    raise RuntimeError("Actuator file '"+model+".acm' not found")

#-------------------------------------------------------------------------------

def Sensor(name, model, **kargs):
  sensorFile = framework.findFile(model+".sem")
  if sensorFile:
    context = {}
    parameters = {}
    execfile(sensorFile, context, parameters)
    parameters.update(kargs)

    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.sensors."+globals.world.physics, type,
      globals.world, name, **parameters)
  else:
    raise RuntimeError("Sensor file '"+model+".sem' not found")

#-------------------------------------------------------------------------------

def Actor(name, model, **kargs):
  actorFile = framework.findFile(model+".acm")
  if actorFile:
    context = {}
    parameters = {}
    execfile(actorFile, context, parameters)
    parameters.update(kargs)

    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.actors."+globals.world.physics, type,
      globals.world, name, **parameters)
  else:
    raise RuntimeError("Actor file '"+model+".acm' not found")

#-------------------------------------------------------------------------------

def Platform(name, model, **kargs):
  platformFile = framework.findFile(model+".pfm")
  if platformFile:
    context = {}
    parameters = {}
    execfile(platformFile, context, parameters)
    parameters.update(kargs)
    
    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.platforms."+globals.world.physics, type,
      globals.world, name, **parameters)
  else:
    raise RuntimeError("Platform file '"+model+".pfm' not found")

#-------------------------------------------------------------------------------

def Controller(model, **kargs):
  controllerFile = framework.findFile(model+".ctl")
  if controllerFile:
    context = {}
    parameters = {}
    execfile(controllerFile, context, parameters)
    parameters.update(kargs)

    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.control", type, globals.world, **parameters)
  else:
    raise RuntimeError("Contoller file '"+model+".ctl' not found")

#-------------------------------------------------------------------------------

def View(name, type, *args, **kargs):
  return Instance("morsel.views", type, globals.world, name, *args, **kargs)

#-------------------------------------------------------------------------------

def Camera(position, object = None, **kargs):
  if object:
    object.attachCamera(position, **kargs)
  else:
    globals.world.scene.attachCamera(position, **kargs)
