from morsel.core import *
from morsel.platforms.ackermann import Ackermann as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Ackermann(Base):
  def __init__(self, world, name, mesh, chassisSolid = None, wheelSolid = None,
      chassisBody = None, wheelBody = None, chassisMass = 0, wheelMass = 0,
      chassisMassOffset = [0, 0, 0], steeringForce = 0, propulsionForce = 0,
      brakingForce = 0, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)
    
    self.steeringForce = steeringForce
    self.propulsionForce = propulsionForce
    self.brakingForce = brakingForce

    self.chassisSolid = Solid(name+"ChassisSolid", chassisSolid, self.chassis,
      body = chassisBody, mass = chassisMass, massOffset = chassisMassOffset,
      parent = self)

    self.wheelSolids = []
    self.wheelJoints = []
    for wheel in self.wheels:
      solid = Solid(name+"WheelSolid", wheelSolid, wheel, body = wheelBody,
        mass = wheelMass, parent = self)
      solid.body.body.setFiniteRotationMode(1)
        
      joint = panda.OdeHinge2Joint(world.world)
      joint.attach(self.chassisSolid.body.body, solid.body.body)
      anchor = solid.geometry.getPos(self.world.scene)
      joint.setAnchor(anchor[0], anchor[1], anchor[2])
      joint.setAxis1(0, 0, 1)
      joint.setAxis2(1, 0, 0)
      joint.setParamFMax(0, self.steeringForce)
      joint.setParamFMax(1, self.propulsionForce)
      joint.setParamStopERP(0, 0.9)
      joint.setParamStopCFM(0, 0)
      joint.setParamStopERP(1, 0.9)
      joint.setParamStopCFM(1, 0)
      joint.setParamSuspensionERP(0, self.getERP(chassisMass, 0.5, 1))
      joint.setParamSuspensionCFM(0, self.getCFM(chassisMass, 0.5, 1))

      if self.isFrontWheel(wheel):
        joint.setParamLoStop(0, -self.maxSteeringAngle*pi/180)
        joint.setParamHiStop(0, self.maxSteeringAngle*pi/180)
      else:
        joint.setParamLoStop(0, 0)
        joint.setParamHiStop(0, 0)
    
      self.wheelSolids.append(solid)
      self.wheelJoints.append(joint)

#-------------------------------------------------------------------------------

  def updateState(self, period):
    for i in range(self.numWheels):
      self.steeringAngles[i] = self.wheelJoints[i].getAngle1()*180/pi
      steeringRate = (-self.command[1]-self.steeringAngles[i])/period
      self.wheelJoints[i].setParamVel(0, steeringRate*pi/180)

      axis = self.wheelJoints[i].getAxis2()
      self.wheelSolids[i].body.body.setFiniteRotationAxis(
        axis[0], axis[1], axis[2])

      if abs(self.command[0]) >= self.epsilon:
        self.wheelJoints[i].setParamFMax(1, self.propulsionForce)
      else:
        self.wheelJoints[i].setParamFMax(1, self.brakingForce)
        
      self.turningRates[i] = self.wheelJoints[i].getAngle2Rate()*180/pi
      turningRate = self.command[0]/self.wheelCircumference[i]*360
      self.wheelJoints[i].setParamVel(1, turningRate*pi/180)

    self.state[0] = 0.5*(self.turningRates[2]*self.wheelCircumference[2]/360+
      self.turningRates[3]*self.wheelCircumference[3]/360)
    self.state[1] = 0.5*(self.steeringAngles[0]+self.steeringAngles[1])

#-------------------------------------------------------------------------------

  def updatePose(self, period):
    self.clearTransform(self.chassis)
    self.pose = [self.getX(), self.getY(), self.getH()]
