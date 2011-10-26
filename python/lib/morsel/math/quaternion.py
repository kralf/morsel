from morsel.core import *

#-------------------------------------------------------------------------------

class Quaternion(panda.Quat):
  def __init__(self, vector = panda.Vec3(1, 0, 0),
      reference = panda.Vec3(1, 0, 0), epsilon = 1e-6):
    panda.Quat.__init__(self)

    l = vector.length()
    dr = -vector.cross(reference)
    lr = dr.length()
    ds = vector.dot(reference)

    if (l >= epsilon) and (lr >= epsilon):
      ijk = dr*sqrt((l-ds)/(2*l))/lr
      r = sqrt((l+ds)/(2*l))

      self.setI(ijk[0])
      self.setJ(ijk[1])
      self.setK(ijk[2])
      self.setR(r)
      