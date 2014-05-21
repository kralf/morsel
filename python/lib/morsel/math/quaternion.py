from morsel.panda import *

from math import *

#-------------------------------------------------------------------------------

class Quaternion(panda.Quat):
  def __init__(self, orientation = [0, 0, 0]):
    panda.Quat.__init__(self)
    
    self.orientation = orientation

#-------------------------------------------------------------------------------

  def getOrientation(self):
    hpr = self.getHpr()
    return [hpr[0], hpr[2], hpr[1]]
  
  def setOrientation(self, orientation):
    self.setHpr(panda.Vec3(orientation[0], orientation[2], orientation[1]))
  
  orientation = property(getOrientation, setOrientation)
  
#-------------------------------------------------------------------------------

  def setFromVectors(self, u, v):
    u = panda.Vec3(u[0], u[1], u[2])
    v = panda.Vec3(v[0], v[1], v[2])
    
    u.normalize()
    v.normalize()
    
    w = u.cross(v)
    w.normalize()
    theta = acos(u.dot(v))*180.0/pi
    
    self.setFromAxisAngle(theta, w)

#-------------------------------------------------------------------------------

  def lookAt(self, direction, up = [0, 0, 1]):
    d = panda.Vec3(direction[0], direction[1], direction[2])
    u = panda.Vec3(up[0], up[1], up[2])
    
    d.normalize()
    u.normalize()
    
    w = d.cross(panda.Vec3(1, 0, 0))
    w.normalize()
    
    quaternion = Quaternion()
    quaternion.setFromVectors([1, 0, 0], direction)
    
    self.setFromVectors(u, w)
    self *= quaternion
    