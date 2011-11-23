from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Mesh(Solid):
  def __init__(self, world, name, mesh, **kargs):
    Solid.__init__(self, world, name, mesh = mesh, geometry = "Box", **kargs)
