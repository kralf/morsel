from morsel.nodes import *

#-------------------------------------------------------------------------------

def Scene(model = None, **kargs):
  module = "nodes"
  if framework.world.physics:
    module += "."+framework.world.physics
  
  scene = framework.createInstance(module, type = "Scene", **kargs)
  if model:
    framework.executeFile(model+".scm")

  return scene

#-------------------------------------------------------------------------------

def Geometry(**kargs):
  return framework.createInstance("geometries", **kargs)

#-------------------------------------------------------------------------------

def Mesh(filename = None, **kargs):
  if filename:
    if isinstance(filename, dict):
      file = {}
      for layer in filename.iterkeys():
        fileroot = filename[layer].rsplit(":", 1)
        file[layer] = framework.findFile(fileroot[0])
        
        if file[layer]:
          if len(fileroot) > 1:
            file[layer] += ":"+fileroot[1]
        else:
          framework.error("Mesh file '"+filename[layer]+"' not found.")
    else:
      fileroot = filename.rsplit(":", 1)
      file = framework.findFile(fileroot[0])
      
      if file:
        if len(fileroot) > 1:
          file += ":"+fileroot[1]
      else:
        framework.error("Mesh file '"+filename+"' not found.")
  else:
    file = None
    
  return framework.createInstance("nodes", type = "Mesh", filename = file,
    **kargs)

#-------------------------------------------------------------------------------

def Object(**kargs):
  module = "nodes"
  if framework.world.physics:
    module += "."+framework.world.physics
    
  return framework.createInstance(module, type = "Object", **kargs)

#-------------------------------------------------------------------------------

def Static(**kargs):
  module = "nodes"
  if framework.world.physics:
    module += "."+framework.world.physics
    
  return framework.createInstance(module, type = "Static", **kargs)

#-------------------------------------------------------------------------------

def Actuator(model = None, **kargs):
  module = "actuators"
  if framework.world.physics:
    module += "."+framework.world.physics

  if model:
    return framework.loadInstance(module, model+".acm", **kargs)
  else:
    return framework.loadInstance(module, **kargs)

#-------------------------------------------------------------------------------

def Sensor(model = None, **kargs):
  module = "sensors"
  if framework.world.physics:
    module += "."+framework.world.physics
    
  if model:
    return framework.loadInstance(module, model+".sem", **kargs)
  else:
    return framework.loadInstance(module, **kargs)

#-------------------------------------------------------------------------------

def Actor(model = None, **kargs):
  module = "actors"
  if framework.world.physics:
    module += "."+framework.world.physics
    
  if model:
    return framework.loadInstance(module, model+".acm", **kargs)
  else:
    return framework.loadInstance(module, **kargs)

#-------------------------------------------------------------------------------

def Platform(model = None, **kargs):
  module = "platforms"
  if framework.world.physics:
    module += "."+framework.world.physics
    
  if model:
    return framework.loadInstance(module, model+".pfm", **kargs)
  else:
    return framework.loadInstance(module, **kargs)

#-------------------------------------------------------------------------------

def View(**kargs):
  return framework.createInstance("views", **kargs)

#-------------------------------------------------------------------------------

def Widget(**kargs):
  return framework.createInstance("widgets", gui = framework.gui, **kargs)

#-------------------------------------------------------------------------------

def Controller(model, **kargs):
  return framework.loadInstance("control", model+".ctl", **kargs)

#-------------------------------------------------------------------------------

def Input(**kargs):
  return framework.createInstance("input", **kargs)

#-------------------------------------------------------------------------------

def Output(**kargs):
  return framework.createInstance("output", **kargs)

#-------------------------------------------------------------------------------

def Light(**kargs):
  return framework.createInstance("light", **kargs)

#-------------------------------------------------------------------------------

def Camera(position = [0, 0, 0], object = None, **kargs):
  if object:
    object.attachCamera(position, **kargs)
  else:
    framework.world.scene.attachCamera(position, **kargs)

#-------------------------------------------------------------------------------

def Path(filename = None, **kargs):
  if filename:
    pathFile = framework.findFile(filename)
    if not pathFile:
      framework.error("Path file '"+filename+"' not found.")
  else:
    pathFile = None

  return framework.createInstance("nodes", type = "Path", filename = pathFile,
    **kargs)
