from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry

#-------------------------------------------------------------------------------

class Ray(Geometry):
  def __init__(self, world, name, solid, start = [0, 0, 0],
      direction = [0, 0, -1], length = 1, **kargs):
    geometry = panda.OdeRayGeom(world.space, length)
    
    Geometry.__init__(self, world, name, solid, geometry = geometry, **kargs)

    geometry.set(self.world.scene.getRelativePoint(self, panda.Point3(*start)),
      self.world.scene.getRelativeVector(self, panda.Vec3(*direction)))
