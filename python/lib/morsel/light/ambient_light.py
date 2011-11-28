from morsel.panda import *
from morsel.nodes import Light

#-------------------------------------------------------------------------------

class AmbientLight(Light):
  def __init__(self, world, name, color = [0.5, 0.5, 0.5, 1], **kargs):
    light = panda.AmbientLight(name+"Light")
    Light.__init__(self, world, name, light, color = color, **kargs)
    