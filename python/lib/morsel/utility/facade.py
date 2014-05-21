from morsel.utility import *

#-------------------------------------------------------------------------------

def Font(filename = None, **kargs):
  if filename:
    fontFile = framework.findFile(filename)
    if not fontFile:
      framework.error("Font file '"+filename+"' not found.")
  else:
    fontFile = None
    
  return framework.createInstance("utility", type = "Font",
    filename = fontFile, **kargs)

#-------------------------------------------------------------------------------

def ShaderProgram(filename = None, **kargs):
  if filename:
    shaderFile = framework.findFile(filename)
    if not shaderFile:
      framework.error("Shader file '"+filename+"' not found.")
  else:
    shaderFile = ""

  return framework.createInstance("utility", type = "ShaderProgram",
    filename = shaderFile, **kargs)
