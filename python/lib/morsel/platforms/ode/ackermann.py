from morsel.core import *
from morsel.platforms.ackermann import Ackermann as Base
from morsel.nodes.facade import Solid, Body

#-------------------------------------------------------------------------------

class Ackermann(Base):
  def __init__(self, world, name, mesh, chassisSolid = None, wheelSolid = None,
      chassisBody = None, wheelBody = None, chassisMass = 0, wheelMass = None,
      wheelSuspension = None, chassisMassOffset = [0, 0, 0], steeringForce = 0,
      propulsionForce = 0, brakingForce = 0, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.wheelSuspension = wheelSuspension
    self.steeringForce = steeringForce
    self.propulsionForce = propulsionForce
    self.brakingForce = brakingForce

    self.solid = Solid(name+"Solid", "Empty", parent = self)
    self.chassisSolid = Solid(name+"ChassisSolid", chassisSolid, self.chassis,
      body = chassisBody, mass = chassisMass, massOffset = chassisMassOffset,
      parent = self.solid)

    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.chassisSolid.body.body, self.solid.body.body)
    joint.set()

    self.minSteeringAngles = self.getSteeringAngles(-self.maxSteeringAngle)
    self.maxSteeringAngles = self.getSteeringAngles(self.maxSteeringAngle)

    self.wheelSolids = []
    self.wheelJoints = []
    for i in range(self.numWheels):
      solid = Solid(name+"WheelSolid", wheelSolid, self.wheels[i],
        body = wheelBody, mass = wheelMass[i], parent = self.chassisSolid)

      joint = panda.OdeHinge2Joint(world.world)
      joint.attach(self.chassisSolid.body.body, solid.body.body)
      anchor = solid.mesh.getPos(self.world.scene)
      joint.setAnchor(anchor[0], anchor[1], anchor[2])
      axis1 = panda.Vec3(0, 0, 1)
      joint.setAxis1(self.world.scene.getRelativeVector(self, axis1))
      axis2 = panda.Vec3(0, -1, 0)
      joint.setAxis2(self.world.scene.getRelativeVector(self, axis2))
      joint.setParamFMax(1, self.propulsionForce)
      joint.setParamLoStop(0, 0)
      joint.setParamHiStop(0, 0)
      joint.setParamStopERP(0, 0.9)
      joint.setParamStopCFM(0, 0)
      joint.setParamStopERP(1, 0.9)
      joint.setParamStopCFM(1, 0)
      joint.setParamSuspensionERP(0, world.getERP(chassisMass,
        wheelSuspension[i], 1))
      joint.setParamSuspensionCFM(0, world.getCFM(chassisMass,
        wheelSuspension[i], 1))

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

    self.state[0] = self.solid.body.body.getLinearVel().project(
      panda.Quat(self.solid.body.body.getQuaternion()).xform(
      panda.Vec3(1, 0, 0))).length()
    self.state[1] = -self.getSteeringAngle(self.steeringAngles)

    position = self.solid.position
    orientation = self.solid.orientation
    self.pose = [position[0], position[1], position[2],
      orientation[0], orientation[1], orientation[2]]

    Base.updatePhysics(self, period)

#-------------------------------------------------------------------------------

  def attachCamera(self, *args, **kargs):
    self.chassis.attachCamera(*args, **kargs)
    