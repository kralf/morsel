from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Plane(Solid):
  def __init__(self, world, name, mesh, **kargs):
    Solid.__init__(self, world, name, mesh = mesh, geometry = "Plane",
      **kargs)
  