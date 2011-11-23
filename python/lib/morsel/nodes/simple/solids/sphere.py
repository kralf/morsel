from morsel.nodes.simple.solid import Solid

#-------------------------------------------------------------------------------

class Sphere(Solid):
  def __init__(self, world, name, mesh, **kargs):
    Solid.__init__(self, world, name, mesh = mesh, geometry = "Sphere",
      **kargs)
