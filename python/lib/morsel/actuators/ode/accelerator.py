from morsel.panda import *
from morsel.math import *
from morsel.actuators import Accelerator as Base
from morsel.nodes.facade import Solid

#-------------------------------------------------------------------------------

class Accelerator(Base):
  def __init__(self, world, name, mesh, solid = None, accelerationForce = [0]*6,
      decelerationForce = [0]*6, epsilon = 1e-6, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    self.accelerationForce = accelerationForce
    self.decelerationForce = decelerationForce
    self.epsilon = epsilon

    self.linearMotor = panda.OdeLMotorJoint(world.world)
    self.linearMotor.attach(self.solid.body.body, None)
    self.linearMotor.setNumAxes(3)
    self.linearMotor.setAxis(0, 0, 1, 0, 0)
    self.linearMotor.setAxis(1, 0, 0, 1, 0)
    self.linearMotor.setAxis(2, 0, 0, 0, 1)
    for i in range(0, 3):
      self.linearMotor.setParamFMax(i, self.accelerationForce[i])
      self.linearMotor.setParamStopERP(i, 0.9)
      self.linearMotor.setParamStopCFM(i, 0)

    self.angularMotor = panda.OdeAMotorJoint(world.world)
    self.angularMotor.attach(self.solid.body.body, None)
    self.angularMotor.setMode(1)
    self.angularMotor.setAxis(0, 0, 0, 0, 1)
    self.angularMotor.setAxis(1, 0, 0, 1, 0)
    self.angularMotor.setAxis(2, 0, 1, 0, 0)
    for i in range(0, 3):
      self.angularMotor.setParamFMax(i, self.accelerationForce[3+i])
      self.angularMotor.setParamStopERP(i, 0.9)
      self.angularMotor.setParamStopCFM(i, 0)

    self.ray = Solid(name+"Ray", "Ray", body = "Empty", parent = self.solid)
    joint = panda.OdeFixedJoint(world.world)
    joint.attach(self.ray.body.body, self.solid.body.body)
    joint.set()
    self.ray.geometry.geometry.collide(self.collide)

#-------------------------------------------------------------------------------

  def collide(self, contact):
    surface = contact.getSurface()
    surface.setMu(0)
    contact.setSurface(surface)

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    for i in range(0, 3):
      self.linearMotor.setParamVel(i, self.command[i])
      if abs(self.command[i]) >= self.epsilon:
        self.linearMotor.setParamFMax(i, self.accelerationForce[i])
      else:
        self.linearMotor.setParamFMax(i, self.decelerationForce[i])
        
    for i in range(0, 3):
      self.angularMotor.setParamVel(i, self.command[3+i]*pi/180)
      if abs(self.command[3+i]) >= self.epsilon:
        self.angularMotor.setParamFMax(i, self.accelerationForce[3+i])
      else:
        self.angularMotor.setParamFMax(i, self.decelerationForce[3+i])

    self.solid.body.body.setQuaternion(panda.Quat())
    self.solid.body.body.setAngularVel(0, 0, 0)
    self.solid.body.body.setTorque(0, 0, 0)

    self.state[0:3] = self.solid.body.translationalVelocity
    self.state[3:6] = self.solid.body.rotationalVelocity
