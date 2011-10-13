from morsel.core import *

import morsel.control

#-------------------------------------------------------------------------------

def Controller(model, **kargs):
  controllerFile = framework.findFile(model+".ctl")
  if controllerFile:
    context = {}
    parameters = kargs
    execfile(controllerFile, context, parameters)

    type = parameters["type"]
    del parameters["type"]

    return Instance("morsel.control", type, **parameters)
  else:
    raise RuntimeError("Contoller file '"+model+".ctl' not found")
