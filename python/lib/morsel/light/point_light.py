from morsel.panda import *
from morsel.nodes.light import Light

#-------------------------------------------------------------------------------

class PointLight(Light):
  def __init__(self, attenuation = None, **kargs):
    super(PointLight, self).__init__(**kargs)

    self.light = panda.PointLight("Light")
    if attenuation:
      self.attenuation = attenuation

#-------------------------------------------------------------------------------

  def getAttenuation(self):
    attenuation = self.light.getAttenuation()
    return [attenuation[0], attenuation[1], attenuation[2]]

  def setAttenuation(self, attenuation):
    self.light.setAttenuation(panda.Vec3(*attenuation))

  attenuation = property(getAttenuation, setAttenuation)
  