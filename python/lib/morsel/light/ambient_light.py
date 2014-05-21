from morsel.panda import *
from morsel.nodes.light import Light

#-------------------------------------------------------------------------------

class AmbientLight(Light):
  def __init__(self, color = [0.5, 0.5, 0.5, 1], **kargs):
    super(AmbientLight, self).__init__(color = color, **kargs)
    
    self.light = panda.AmbientLight("Light")
