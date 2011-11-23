from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Empty(Solid):
  def __init__(self, world, name, mesh = None, body = "Empty", **kargs):
    Solid.__init__(self, world, name, mesh = mesh, geometry = "Empty",
      body = body, **kargs)
