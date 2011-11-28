from morsel.panda import *
from morsel.nodes import Light

#-------------------------------------------------------------------------------

class PointLight(Light):
  def __init__(self, world, name, attenuation = None, **kargs):
    light = panda.PointLight(name+"Light")
    Light.__init__(self, world, name, light, **kargs)

    if attenuation:
      self.attenuation = attenuation

#-------------------------------------------------------------------------------

  def getAttenuation(self):
    attenuation = self.light.getAttenuation()
    return [attenuation[0], attenuation[1], attenuation[2]]

  def setAttenuation(self, attenuation):
    self.light.setAttenuation(panda.Vec3(*attenuation))

  attenuation = property(getAttenuation, setAttenuation)
  