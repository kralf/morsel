from morsel.panda import *
from morsel.math import *
from morsel.geometries.ray import Ray as Base
from morsel.nodes.ode.solid import Solid

#-------------------------------------------------------------------------------

class Ray(Solid, Base):
  def __init__(self, **kargs):
    super(Ray, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def getMesh(self):
    mesh = Base.getMesh(self)
    mesh.orientation = [0, 180, 0]
    
    return mesh
    
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def fit(self, node):
    Base.fit(self, node)

    position = panda.Vec3(*self.origin)+panda.Vec3(*self.direction)*self.length
    self.position = [position[0], position[1], position[2]]
    
    self.geometry = panda.OdeRayGeom(node.world.space, self.globalLength)
    