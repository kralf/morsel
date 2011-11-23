from morsel.panda import *
from morsel.nodes.simple.geometry import Geometry

#-------------------------------------------------------------------------------

class Sphere(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      scale = [1, 1, 1], **kargs):
    geometry = panda.CollisionSphere(position[0], position[1], position[2],
      0.5*max(scale))

    Geometry.__init__(self, world, name, solid, geometry, position = position,
      scale = scale, **kargs)
