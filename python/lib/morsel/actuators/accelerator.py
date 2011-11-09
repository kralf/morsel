from morsel.panda import *
from morsel.math import *
from morsel.nodes import Actuator
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Accelerator(Actuator):
  def __init__(self, world, name, mesh, maxVelocity = [0]*6, **kargs):
    self.maxVelocity = maxVelocity

    limits = []
    for limit in maxVelocity:
      limits.append((-abs(limit), abs(limit)))
    Actuator.__init__(self, world, name, limits = limits,  **kargs)
    
#-------------------------------------------------------------------------------

  def getTranslationalVelocity(self):
    return self.state[0:3]

  def setTranslationalVelocity(self, translationalVelocity):
    self.command[0:3] = translationalVelocity

  translationalVelocity = property(getTranslationalVelocity,
    setTranslationalVelocity)

#-------------------------------------------------------------------------------

  def getRotationalVelocity(self):
    return self.state[3:6]

  def setRotationalVelocity(self, rotationalVelocity):
    self.command[3:6] = rotationalVelocity

  rotationalVelocity = property(getRotationalVelocity, setRotationalVelocity)
