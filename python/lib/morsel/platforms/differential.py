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

    self.wheelAngles = []
    for i in range(self.numWheels):
      wheelPosition = panda.Vec3(self.chassis.getRelativePoint(self.wheels[i],
        panda.Vec3(0, 0, 0)))
      wheelPosition[2] = 0
      wheelPosition.normalize()
      
      self.wheelAngles.append(panda.Vec3(1, 0, 0).signedAngleDeg(
        wheelPosition, panda.Vec3(0, 0, 1)))

    self.numCasters = len(casterWheels)
    self.casterAngles = [0]*self.numCasters
    
    self.casterCranks = []
    self.casterWheels = []
    self.casterDistance = []
    self.casterDepth = []
    self.casterLength = []
    self.casterYaw = []

    for i in range(self.numCasters):
      crankModel = self.mesh.find("**/"+casterCranks[i])
      if not crankModel.isEmpty():
        crank = Mesh(name+"CrankMesh", model = crankModel, parent = self)

        wheel = self.wheels[wheels.index(casterWheels[i])]
        self.casterWheels.append(wheel)

        self.casterCranks.append(crank)
        casterPosition = crank.getPos(self)
        casterPosition[2] = 0
        self.casterDistance.append(casterPosition.length())
        wheelPosition = wheel.getPos(crank)
        self.casterDepth.append(wheelPosition[2])
        wheelPosition[2] = 0
        self.casterLength.append(wheelPosition.length())
        self.casterYaw.append(crank.yaw)
      else:
        raise RuntimeError("Crank model '"+casterCranks[i]+"' not found")

    self.wheelDistance = self.getWheelDistance(0, 1)

#-------------------------------------------------------------------------------

  def getCasterRates(self, translationalVelocity, rotationalVelocity):
    casterRates = [0]*self.numCasters

    for i in range(self.numCasters):
      psi = self.casterAngles[i]*pi/180
      casterRates[i] = ((1/self.casterLength[i]*(-rotationalVelocity*
        pi/180*(self.casterDistance[i]*cos(psi)+self.casterLength[i])-
        translationalVelocity*sin(psi)))*180/pi)

    return casterRates

#-------------------------------------------------------------------------------

  def getTurningOrientation(self, wheel):
    i = self.wheels.index(wheel)

    if self.wheelAngles[i] < 0:
      return 1
    else:
      return -1

#-------------------------------------------------------------------------------

  def getTurningRates(self, translationalVelocity, rotationalVelocity):
    turningRates = [0]*self.numWheels
    turningOrientations = [0]*self.numWheels

    for i in range(self.numWheels):
      if self.isCasterWheel(self.wheels[i]):
        j = self.casterWheels.index(self.wheels[i])
        psi = self.casterAngles[j]*pi/180

        turningRates[i] = ((translationalVelocity*cos(psi)-
          rotationalVelocity*pi/180*self.casterDistance[j]*sin(psi))/
          self.wheelRadius[i]*180/pi)
      else:
        turningRates[i] = (((translationalVelocity+
          self.getTurningOrientation(self.wheels[i])*
          0.5*self.wheelDistance*rotationalVelocity*pi/180)/
          self.wheelRadius[i])*180/pi)
        turningOrientations[i] = self.getTurningOrientation(self.wheels[i])

    return turningRates

#-------------------------------------------------------------------------------

  def isCasterWheel(self, wheel):
    return wheel in self.casterWheels

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    Wheeled.updatePhysics(self, period)

    for i in range(self.numCasters):
      j = self.wheels.index(self.casterWheels[i])
      self.steeringAngles[j] = self.casterAngles[i]

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    Wheeled.updateGraphics(self)

    for i in range(self.numCasters):
      self.casterCranks[i].yaw = self.casterYaw[i]+self.casterAngles[i]
      self.casterWheels[i].setPos(self.casterCranks[i],
        panda.Vec3(-self.casterLength[i], 0, self.casterDepth[i]))
