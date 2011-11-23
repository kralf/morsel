from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Empty(Solid):
  def __init__(self, world, name, mesh, **kargs):
    Solid.__init__(self, world, name, mesh = mesh, geometry = "Empty",
      **kargs)
