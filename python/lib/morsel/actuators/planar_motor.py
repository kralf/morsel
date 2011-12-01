from morsel.panda import *
from morsel.math import *
from morsel.nodes import Actuator
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class PlanarMotor(Actuator):
  def __init__(self, world, name, mesh, base = None, hideBase = False,
      maxVelocity = [0, 0, 0], **kargs):
    self.hideBase = hideBase
    self.maxVelocity = maxVelocity

    limits = []
    for limit in maxVelocity:
      limits.append((-abs(limit), abs(limit)))
    Actuator.__init__(self, world, name, limits = limits,  **kargs)

    baseModel = mesh
    if base:
      baseModel = mesh.find("**/"+base)
    if not baseModel.isEmpty():
      self.base = Mesh(name = name+"Mesh", model = baseModel, parent = self)
      if self.hideBase:
        self.base.hide()
    else:
      framework.error("Base model '"+base+"' not found")

#-------------------------------------------------------------------------------

  def getTranslationalVelocity(self):
    return self.state[0:2]

  def setTranslationalVelocity(self, translationalVelocity):
    self.command[0:2] = translationalVelocity

  translationalVelocity = property(getTranslationalVelocity,
    setTranslationalVelocity)

#-------------------------------------------------------------------------------

  def getRotationalVelocity(self):
    return self.state[2]

  def setRotationalVelocity(self, rotationalVelocity):
    self.command[2] = rotationalVelocity[0]

  rotationalVelocity = property(getRotationalVelocity, setRotationalVelocity)
