from morsel.panda import *
from morsel.nodes.simple.geometry import Geometry
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Ray(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      orientation = [0, 0, 0], scale = [1, 1, 1], **kargs):
    geometry = panda.CollisionRay()

    position[2] += 0.5*scale[2]
    geometry.setOrigin(*position)
    geometry.setDirection(0, 0, -1)

    Geometry.__init__(self, world, name, solid, geometry = geometry,
      position = position, orientation = orientation, scale = scale,  **kargs)
