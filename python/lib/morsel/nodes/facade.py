from morsel.world import globals
from morsel.nodes import *

#-------------------------------------------------------------------------------

def Text(**kargs):
  return framework.createInstance("nodes", type = "Text",
    world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Mesh(filename = None, **kargs):
  if filename:
    if isinstance(filename, dict):
      meshFile = {}
      for layer in filename.iterkeys():
        meshFile[layer] = framework.findFile(filename[layer])
        if not meshFile[layer]:
          framework.error("Mesh file '"+filename[layer]+"' not found")
    else:
      meshFile = framework.findFile(filename)
      if not meshFile:
        framework.error("Mesh file '"+filename+"' not found")
  else:
    meshFile = None
    
  return framework.createInstance("nodes", type = "Mesh",
    world = framework.world, filename = meshFile, **kargs)

#-------------------------------------------------------------------------------

def Light(**kargs):
  return framework.createInstance("light", world = framework.world,
    **kargs)

#-------------------------------------------------------------------------------

def Path(filename = None, **kargs):
  if filename:
    pathFile = framework.findFile(filename)
    if not pathFile:
      framework.error("Path file '"+filename+"' not found")
  else:
    pathFile = None

  return framework.createInstance("nodes", type = "Path",
    world = framework.world, filename = pathFile, **kargs)

#-------------------------------------------------------------------------------

def Collider(**kargs):
  return framework.createInstance("nodes."+framework.world.physics,
    type = "Collider", world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Solid(**kargs):
  return framework.createInstance( "nodes."+framework.world.physics+".solids",
    world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Static(**kargs):
  return framework.createInstance("nodes", type = "Static",
    world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Scene(model = None, **kargs):
  scene = framework.createInstance("nodes."+framework.world.physics,
    type = "Scene", world = framework.world, **kargs)
  if model:
    framework.executeFile(model+".scm")

  return scene

#-------------------------------------------------------------------------------

def Actuator(model, **kargs):
  return framework.loadInstance("actuators."+framework.world.physics,
    model+".acm", world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Sensor(model, **kargs):
  return framework.loadInstance("sensors."+framework.world.physics,
    model+".sem", world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Actor(model, **kargs):
  return framework.loadInstance("actors."+framework.world.physics,
    model+".acm", world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Platform(model, **kargs):
  return framework.loadInstance("platforms."+framework.world.physics,
    model+".pfm", world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def Controller(model, **kargs):
  return framework.loadInstance("control", model+".ctl",
    world = framework.world, **kargs)

#-------------------------------------------------------------------------------

def View(**kargs):
  return framework.createInstance("views", world = framework.world,
    **kargs)

#-------------------------------------------------------------------------------

def Input(**kargs):
  return framework.createInstance("input", world = framework.world,
    **kargs)

#-------------------------------------------------------------------------------

def Output(**kargs):
  return framework.createInstance("output", world = framework.world,
    **kargs)

#-------------------------------------------------------------------------------

def Camera(position, object = None, **kargs):
  if object:
    object.attachCamera(position, **kargs)
  else:
    framework.world.scene.attachCamera(position, **kargs)
