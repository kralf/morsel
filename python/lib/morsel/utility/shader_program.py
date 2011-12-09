from morsel.panda import *
from morsel.morselc import ShaderProgram as CShaderProgram

#-------------------------------------------------------------------------------

class ShaderProgram(CShaderProgram):
  def __init__(self, filename = None, node = None, **kargs):
    if filename:
      self.filename = framework.findFile(filename)
      if not self.filename:
        framework.error("Shader file '"+filename+"' not found")
    else:
      self.filename = ""
      
    CShaderProgram.__init__(self, self.filename)

    if node:
      shader = self.make()
      node.setShader(shader)
