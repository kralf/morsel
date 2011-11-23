from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Box(Solid):
  def __init__(self, world, name, mesh, **kargs):
    Solid.__init__(self, world, name, mesh = mesh, geometry = "Box",
      **kargs)
