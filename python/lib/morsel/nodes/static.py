from facade import Mesh
from object import Object

#-------------------------------------------------------------------------------

class Static(Object):
  def __init__(self, mesh = None, flatten = True, **kargs):
    super(Static, self).__init__(**kargs)
    
    if mesh:
      self.mesh = Mesh(filename = mesh, flatten = flatten)
    