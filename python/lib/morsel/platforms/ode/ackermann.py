from morsel.core import *
from morsel.platforms.ackermann import Ackermann as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Ackermann(Base):
  def __init__(self, world, name, mesh, chassisSolid = None, wheelSolid = None,
      chassisBody = None, wheelBody = None, chassisMass = 0, wheelMass = None,
      chassisMassOffset = [0, 0, 0], steeringForce = 0, propulsionForce = 0,
      brakingForce = 0, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)
    
    self.steeringForce = steeringForce
    self.propulsionForce = propulsionForce
    self.brakingForce = brakingForce

    self.chassisSolid = Solid(name+"ChassisSolid", chassisSolid, self.chassis,
      body = chassisBody, mass = chassisMass, massOffset = chassisMassOffset,
      parent = self)

    self.nullBody = panda.OdeBody(world.world)
    self.nullBody.setPosition(self.chassis.getPos(self.world.scene))
    self.nullBody.setQuaternion(self.chassis.getQuat(self.world.scene))
    self.nullJoint = panda.OdeFixedJoint(world.world)
    self.nullJoint.attach(self.chassisSolid.body.body, self.nullBody)
    self.nullJoint.set()

    self.minSteeringAngles = self.getSteeringAngles(-self.maxSteeringAngle)
    self.maxSteeringAngles = self.getSteeringAngles(self.maxSteeringAngle)

    self.wheelSolids = []
    self.wheelJoints = []
    for i in range(self.numWheels):
      solid = Solid(name+"WheelSolid", wheelSolid, self.wheels[i],
        body = wheelBody, mass = wheelMass[i], parent = self)
        
      joint = panda.OdeHinge2Joint(world.world)
      joint.attach(self.chassisSolid.body.body, solid.body.body)
      anchor = solid.geometry.getPos(self.world.scene)
      joint.setAnchor(anchor[0], anchor[1], anchor[2])
      joint.setAxis1(0, 0, 1)
      joint.setAxis2(1, 0, 0)
      joint.setParamFMax(1, self.propulsionForce)
      joint.setParamLoStop(0, 0)
      joint.setParamHiStop(0, 0)
      joint.setParamStopERP(0, 0.9)
      joint.setParamStopCFM(0, 0)
      joint.setParamStopERP(1, 0.9)
      joint.setParamStopCFM(1, 0)
      joint.setParamSuspensionERP(0, world.getERP(chassisMass, 0.5, 1))
      joint.setParamSuspensionCFM(0, world.getCFM(chassisMass, 0.5, 1))

      if self.isFrontWheel(self.wheels[i]):
        joint.setParamFMax(0, self.steeringForce)
      else:
        joint.setParamFMax(0, 0)
    
      self.wheelSolids.append(solid)
      self.wheelJoints.append(joint)

#-------------------------------------------------------------------------------
    
  def updatePhysics(self, period):
    steeringAngles = self.getSteeringAngles(-self.command[1])

    for i in range(self.numWheels):
      self.steeringAngles[i] = self.wheelJoints[i].getAngle1()*180/pi
      steeringError = self.steeringAngles[i]-steeringAngles[i]
      steeringRate = -steeringError/period
      self.wheelJoints[i].setParamVel(0, steeringRate*pi/180)
      self.wheelJoints[i].setParamLoStop(0, steeringAngles[i]*pi/180)
      self.wheelJoints[i].setParamHiStop(0, steeringAngles[i]*pi/180)

      if abs(self.command[0]) >= self.epsilon:
        self.wheelJoints[i].setParamFMax(1, self.propulsionForce)
      else:
        self.wheelJoints[i].setParamFMax(1, self.brakingForce)
        
      self.turningRates[i] = self.wheelJoints[i].getAngle2Rate()*180/pi
      turningRate = self.command[0]/self.wheelCircumference[i]*360
      self.wheelJoints[i].setParamVel(1, turningRate*pi/180)

    self.state[0] = self.nullBody.getLinearVel().project(
      panda.Quat(self.nullBody.getQuaternion()).xform(
      panda.Vec3(1, 0, 0))).length()
    self.state[1] = panda.Quat(self.nullBody.getQuaternion()).xform(
      self.nullBody.getAngularVel())[2]*180.0/pi

    position = self.nullBody.getPosition()
    orientation = panda.Quat(self.nullBody.getQuaternion()).getHpr()
    self.pose = [position[0], position[1], position[2],
      orientation[0], orientation[1], orientation[2]]

    Base.updatePhysics(self, period)

#-------------------------------------------------------------------------------

  def attachCamera(self, *args, **kargs):
    self.chassis.attachCamera(*args, **kargs)
    