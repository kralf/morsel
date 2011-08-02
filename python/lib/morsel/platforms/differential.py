from morsel.core import *
from morsel.platforms import Wheeled
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Differential(Wheeled):
  def __init__(self, world, name, mesh, wheels = [], casterCranks = [],
      casterWheels = [], maxTranslationalVelocity = 0,
      maxRotationalVelocity = 0, epsilon = 1e-6, **kargs):
    self.maxTranslationalVelocity = maxTranslationalVelocity
    self.maxRotationalVelocity = maxRotationalVelocity
    self.epsilon = epsilon
    
    limits = [(-maxTranslationalVelocity, maxTranslationalVelocity),
      (-maxRotationalVelocity, maxRotationalVelocity)]      
    Wheeled.__init__(self, world, name, mesh, wheels = wheels, limits = limits,
      **kargs)

    self.numCasters = len(casterWheels)
    self.casterAngles = [0]*self.numCasters
    
    self.casterCranks = []
    self.casterWheels = []
    self.casterDistance = []
    self.casterLength = []
    self.casterYaw = []

    for i in range(len(casterCranks)):
      crankModel = self.mesh.find("**/"+casterCranks[i])
      if not crankModel.isEmpty():
        crank = Mesh(name+"CrankMesh", model = crankModel, parent = self)

        wheel = self.wheels[wheels.index(casterWheels[i])]
        wheel.setParent(crank, True)
        self.casterWheels.append(wheel)

        self.casterCranks.append(crank)
        self.casterDistance.append(crank.getPos(self).length())
        self.casterLength.append(wheel.getPos(crank).length())
        self.casterYaw.append(crank.yaw)
      else:
        raise RuntimeError("Crank model '"+casterCranks[i]+"' not found")

    self.wheelDistance = self.getWheelDistance(0, 1)

#-------------------------------------------------------------------------------

  def isCasterWheel(self, wheel):
    return wheel in self.casterWheels

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    Wheeled.updateGraphics(self)

    for i in range(self.numCasters):
      self.casterCranks[i].yaw = self.casterYaw[i]+self.casterAngles[i]
