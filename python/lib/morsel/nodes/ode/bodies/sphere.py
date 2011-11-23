from morsel.panda import *
from morsel.nodes.ode.body import Body
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Sphere(Body):
  def __init__(self, world, name, solid, mass = 0, scale = [1, 1, 1],
      **kargs):
    radius = 0.5*max(scale)
    sphere = panda.OdeMass()
    sphere.setSphereTotal(mass, radius)

    Body.__init__(self, world, name, solid, mass = sphere,
      scale = [2*radius]*3, **kargs)
