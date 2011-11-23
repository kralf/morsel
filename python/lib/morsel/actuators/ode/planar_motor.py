from morsel.panda import *
from morsel.math import *
from morsel.actuators import PlanarMotor as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class PlanarMotor(Base):
  def __init__(self, world, name, mesh, baseSolid = None, baseBody = None,
      baseMass = None, accelerationForce = [0, 0, 0],
      decelerationForce = [0, 0, 0], epsilon = 1e-6, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.accelerationForce = accelerationForce
    self.decelerationForce = decelerationForce
    self.epsilon = epsilon

    self.baseSolid = Solid(name+"BaseSolid", baseSolid, self.base,
      body = baseBody, mass = baseMass, parent = self.solid)
    self.baseSolid.geometry.geometry.collide(self.collide)
    
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.solid.body.body, self.baseSolid.body.body)
    joint.set()
    
    self.linearMotor = panda.OdeLMotorJoint(world.world)
    self.linearMotor.attach(self.solid.body.body, None)
    self.linearMotor.setNumAxes(2)
    self.linearMotor.setAxis(0, 0, 1, 0, 0)
    self.linearMotor.setAxis(1, 0, 0, 1, 0)
    for i in [0, 1]:
      self.linearMotor.setParamFMax(i, self.accelerationForce[i])
      self.linearMotor.setParamStopERP(i, 0.9)
      self.linearMotor.setParamStopCFM(i, 0)

    self.angularMotor = panda.OdeAMotorJoint(world.world)
    self.angularMotor.attach(self.solid.body.body, None)
    self.angularMotor.setMode(1)
    self.angularMotor.setAxis(0, 0, 0, 0, 1)
    self.angularMotor.setAxis(1, 0, 0, 1, 0)
    self.angularMotor.setAxis(2, 0, 1, 0, 0)
    self.angularMotor.setParamFMax(0, self.accelerationForce[2])
    self.angularMotor.setParamStopERP(0, 0.9)
    self.angularMotor.setParamStopCFM(0, 0)
    for i in [1, 2]:
      self.angularMotor.setParamFMax(i, 1e6)
      self.angularMotor.setParamStopERP(i, 0.9)
      self.angularMotor.setParamStopCFM(i, 0)

#-------------------------------------------------------------------------------

  def collide(self, contact):
    surface = contact.getSurface()
    surface.setMode(panda.OdeSurfaceParameters.MFContactApprox1 |
      panda.OdeSurfaceParameters.MFContactFDir1 |
      panda.OdeSurfaceParameters.MFContactMu2)
    contact.setFdir1(self.world.scene.getRelativeVector(self.solid,
      panda.Vec3(0, 1, 0)))

    if abs(self.command[0]) >= self.epsilon:
      surface.setMu2(0)
    if abs(self.command[1]) >= self.epsilon:
      surface.setMu(0)
    if abs(self.command[2]) >= self.epsilon:
      surface.setMu(0)
      surface.setMu2(0)

    contact.setSurface(surface)

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    command = self.world.scene.getRelativeVector(self.solid,
      panda.Vec3(self.command[0], self.command[1], 0))
    accelerationForce = self.world.scene.getRelativeVector(self.solid,
      panda.Vec3(self.accelerationForce[0], self.accelerationForce[1], 0))
    decelerationForce = self.world.scene.getRelativeVector(self.solid,
      panda.Vec3(self.decelerationForce[0], self.decelerationForce[1], 0))
    
    for i in [0, 1]:
      self.linearMotor.setParamVel(i, command[i])
      if abs(command[i]) >= self.epsilon:
        self.linearMotor.setParamFMax(i, abs(accelerationForce[i]))
      else:
        self.linearMotor.setParamFMax(i, abs(decelerationForce[i]))
        
    self.angularMotor.setParamVel(0, self.command[2]*pi/180)
    if abs(self.command[2]) >= self.epsilon:
      self.angularMotor.setParamFMax(i, self.accelerationForce[2])
    else:
      self.angularMotor.setParamFMax(i, self.decelerationForce[2])

    quaternion = panda.Quat(self.solid.body.body.getQuaternion())
    orientation = quaternion.getHpr()
    rotationalVelocity = self.solid.body.getRotationalVelocity(
      self.world.scene)
    torque = [0, 0, 0]
    for i in [1, 2]:
      orientation[i] = 0
      rotationalVelocity[i] = 0
    quaternion.setHpr(orientation)
    self.solid.body.body.setQuaternion(quaternion)
    self.solid.body.setRotationalVelocity(rotationalVelocity,
      self.world.scene)
    self.solid.body.setTorque(torque, self.world.scene)

    self.state[0:2] = self.solid.body.translationalVelocity[0:2]
    self.state[2] = self.solid.body.rotationalVelocity[0]
    