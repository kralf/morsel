from morsel.core import *
from morsel.nodes import Platform
from morsel.nodes.facade import Mesh

#-------------------------------------------------------------------------------

class Wheeled(Platform):
  def __init__(self, world, name, mesh, chassis = None, wheels = [], **kargs):
    Platform.__init__(self, world, name, **kargs)

    self.numWheels = len(wheels)
    self.turningRates = [0]*self.numWheels
    self.steeringAngles = [0]*self.numWheels

    self.mesh = Mesh(name+"Mesh", filename = mesh, parent = self)
    self.chassis = None
    self.wheels = []
    self.wheelRadius = []
    self.wheelCircumference = []
    self.wheelYaw = []
    self.wheelRoll = []

    chassisModel = self.mesh.find("**/"+chassis)
    if not chassisModel.isEmpty():
      self.chassis = Mesh(name+"ChassisMesh", model = chassisModel,
        parent = self)
    else:
      raise RuntimeError("Chassis model '"+chassis+"' not found")

    for wheel in wheels:
      wheelModel = self.mesh.find("**/"+wheel)
      if not wheelModel.isEmpty():
        wheel = Mesh(name+"WheelMesh", model = wheelModel, parent = self)

        p0, p1 = wheel.getTightBounds()
        dx = abs(p1[0]-p0[0])
        dz = abs(p1[2]-p0[2])
        radius = 0.5*max(dx, dz)
        
        self.wheels.append(wheel)
        self.wheelRadius.append(radius)
        self.wheelCircumference.append(2*pi*radius)
        self.wheelYaw.append(wheel.yaw)
        self.wheelRoll.append(wheel.pitch)
      else:
        raise RuntimeError("Wheel model '"+wheel+"' not found")
    
#-------------------------------------------------------------------------------

  def getWheelDistance(self, i, j):
    vector = self.wheels[i].getPos(render)-self.wheels[j].getPos(render)
    return vector.length()

#-------------------------------------------------------------------------------

  def setRatesFromVelocities(self, velocities):
    for i in range(self.numWheels):
      self.turningRates[i] = velocities[i]/self.wheelCircumference[i]*360

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    for i in range(self.numWheels):
      self.wheelRoll[i] += self.turningRates[i]*period
      self.wheelRoll[i] = positiveAngle(self.wheelRoll[i])

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    Platform.updateGraphics(self)

    for i in range(self.numWheels):
      self.wheels[i].yaw = self.wheelYaw[i]+self.steeringAngles[i]
      self.wheels[i].roll = self.wheelRoll[i]
