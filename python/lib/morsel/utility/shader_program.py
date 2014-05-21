from morsel.panda import *
from morsel.morselc import ShaderProgram as CShaderProgram

#-------------------------------------------------------------------------------

class ShaderProgram(CShaderProgram):
  def __init__(self, filename = None, node = None, **kargs):
    super(ShaderProgram, self).__init__(filename)

    self.filename = filename
    if node:
      shader = self.make()
      node.setShader(shader)
