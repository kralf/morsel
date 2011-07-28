from morsel.core import *
from morsel.nodes import Node, Mesh, Platform
from morsel.nodes.facade import Mesh as _Mesh

#-------------------------------------------------------------------------------

class Wheeled(Platform):
  def __init__(self, world, name, mesh, wheels = [], **kargs):
    Platform.__init__(self, world, name, **kargs)

    self.numWheels = len(wheels)
    self.turningRates = [0]*self.numWheels
    self.steeringAngles = [0]*self.numWheels

    self.chassis = _Mesh(name+"ChassisMesh", filename = mesh, parent = self)
    self.wheels = []
    self.wheelRadius = []
    self.wheelCircumference = []
    self.wheelYaw = []
    self.wheelRoll = []

    for wheel in wheels:
      wheelModel = self.chassis.find("**/"+wheel)
      if not wheelModel.isEmpty():
        wheelMesh = Mesh(world, name+"WheelMesh", parent = self)
        wheelMesh.setTransformFromPath(wheelModel)
        wheelMesh.setModel(wheelModel)
        wheelModel.clearTransform()

        p0, p1 = wheelMesh.getTightBounds()
        dx = abs(p1[0]-p0[0])
        dz = abs(p1[2]-p0[2])
        radius = 0.5*max(dx, dz)
        
        self.wheels.append(wheelMesh)
        self.wheelRadius.append(radius)
        self.wheelCircumference.append(2*pi*radius)
        self.wheelYaw.append(wheelMesh.yaw)
        self.wheelRoll.append(wheelMesh.pitch)
      else:
        raise RuntimeError("Wheel model '"+wheel+"' not found")
    
#-------------------------------------------------------------------------------

  def getWheelDistance(self, i, j):
    vector = self.wheels[i].getPos(render)-self.wheels[j].getPos(render)
    return vector.length()

#-------------------------------------------------------------------------------

  def getERP(self, mass, period, damping):
    frequency = 2*pi/period
    delta = self.world.period

    return delta*frequency/(delta*frequency+2*damping)

#-------------------------------------------------------------------------------

  def getCFM(self, mass, period, damping):
    frequency = 2*pi/period
    delta = self.world.period
    
    return self.getERP(mass, period, damping)/(delta*frequency**2*mass)

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
    for i in range(self.numWheels):
      self.wheels[i].yaw = self.wheelYaw[i]+self.steeringAngles[i]
      self.wheels[i].roll = self.wheelRoll[i]
