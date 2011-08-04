from morsel.core import *
from morsel.platforms.differential import Differential as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Differential(Base):
  def __init__(self, world, name, mesh, chassisSolid = None, wheelSolid = None,
      crankSolid = None, chassisBody = None, wheelBody = None,
      crankBody = None, chassisMass = 0, wheelMass = None,
      wheelSuspension = None, crankMass = None, chassisMassOffset = [0, 0, 0],
      propulsionForce = 0, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.wheelSuspension = wheelSuspension
    self.propulsionForce = propulsionForce
    
    self.chassisSolid = Solid(name+"ChassisSolid", chassisSolid, self.chassis,
      body = chassisBody, mass = chassisMass, massOffset = chassisMassOffset,
      parent = self)

    self.nullBody = panda.OdeBody(world.world)
    self.nullBody.setPosition(self.chassisSolid.body.body.getPosition())
    self.nullBody.setQuaternion(panda.Quat(
      self.chassisSolid.body.body.getQuaternion()))
    self.nullJoint = panda.OdeFixedJoint(world.world)
    self.nullJoint.attach(self.chassisSolid.body.body, self.nullBody)
    self.nullJoint.set()

    self.crankSolids = []
    self.crankJoints = []
    for i in range(self.numCasters):
      solid = Solid(name+"CrankSolid", crankSolid, self.casterCranks[i],
        body = crankBody, mass = crankMass[i], parent = self)

      joint = panda.OdeHingeJoint(world.world)
      joint.attach(self.chassisSolid.body.body, solid.body.body)
      anchor = solid.geometry.getPos(self.world.scene)
      joint.setAnchor(anchor[0], anchor[1], anchor[2])
      joint.setAxis(0, 0, 1)
      joint.setParamFMax(0)
      joint.setParamStopERP(0.9)
      joint.setParamStopCFM(0)

      self.crankSolids.append(solid)
      self.crankJoints.append(joint)

    self.wheelSolids = []
    self.wheelJoints = []
    for i in range(self.numWheels):
      solid = Solid(name+"WheelSolid", wheelSolid, self.wheels[i],
        body = wheelBody, mass = wheelMass[i], parent = self)

      joint = panda.OdeHinge2Joint(world.world)
      if self.isCasterWheel(self.wheels[i]):
        j = self.casterWheels.index(self.wheels[i])
        joint.attach(self.crankSolids[j].body.body, solid.body.body)
        joint.setParamFMax(1, 0)
      else:
        joint.attach(self.chassisSolid.body.body, solid.body.body)
        joint.setParamFMax(1, self.propulsionForce)
        
      anchor = solid.geometry.getPos(self.world.scene)
      joint.setAnchor(anchor[0], anchor[1], anchor[2])
      joint.setAxis1(0, 0, 1)
      joint.setAxis2(1, 0, 0)
      joint.setParamFMax(0, 0)
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

      self.wheelSolids.append(solid)
      self.wheelJoints.append(joint)

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    for i in range(self.numCasters):
      self.casterAngles[i] = self.crankJoints[i].getAngle()*180/pi
    
    turningRates = self.getTurningRates(self.command[0], self.command[1])
    for i in range(self.numWheels):
      self.turningRates[i] = self.wheelJoints[i].getAngle2Rate()*180/pi
      if not self.isCasterWheel(self.wheels[i]):
        self.wheelJoints[i].setParamVel(1, turningRates[i]*pi/180)

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
