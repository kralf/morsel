from box import Box

#-------------------------------------------------------------------------------

class Mesh(Box):
  def __init__(self, world, name, mesh, **kargs):
    Box.__init__(self, world, name, mesh, **kargs)
