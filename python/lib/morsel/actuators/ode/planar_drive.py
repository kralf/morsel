from morsel.panda import *
from morsel.nodes.ode.facade import Joint
from morsel.actuators.planar_drive import PlanarDrive as Base
from morsel.actuators.ode.drive import Drive

#-------------------------------------------------------------------------------

class PlanarDrive(Drive, Base):
  def __init__(self, bearingSolid = None, bearingBody = None, bearingMass = 1,
      accelerationForce = [0, 0, 0], decelerationForce = [0, 0, 0], actuated =
      None, epsilon = 1e-6, **kargs):
    super(PlanarDrive, self).__init__(solid = bearingSolid, body = bearingBody,
      mass = bearingMass, **kargs)

    self.accelerationForce = accelerationForce
    self.decelerationForce = decelerationForce
    self.epsilon = epsilon
    
    self.solid.geometry.collide(self.collide)
    self.linearJoint = Joint(type = "LinearMotor", axes = [[1, 0, 0],
      [0, 1, 0]], stopERP = 0.9, stopCFM = 0)
    self.angularJoint = Joint(type = "AngularMotor", stopERP = 0.9,
      stopCFM = 0)

    self.actuated = actuated
      
#-------------------------------------------------------------------------------

  def setActuated(self, actuated):
    if self.body:
      self.linearJoint.detach()
      self.angularJoint.detach()
      
    super(PlanarDrive, self).setActuated(actuated)
    
    if self.body:
      self.linearJoint.attach(self, None)
      self.angularJoint.attach(self, None)
    
  actuated = property(Base.getActuated, setActuated)
  
#-------------------------------------------------------------------------------

  def collide(self, contact):
    command = render.getRelativeVector(self,
      panda.Vec3(self.command[0], self.command[1], 0))
    command[2] = self.command[2]
    
    surface = contact.getSurface()
    surface.setMode(panda.OdeSurfaceParameters.MFContactApprox1 |
      panda.OdeSurfaceParameters.MFContactFDir1 |
      panda.OdeSurfaceParameters.MFContactMu2)
      
    if abs(command[0]) >= self.epsilon:
      surface.setMu2(0)
    if abs(command[1]) >= self.epsilon:
      surface.setMu(0)
    if abs(command[2]) >= self.epsilon:
      surface.setMu(0)
      surface.setMu2(0)
    
    contact.setSurface(surface)
    contact.setFdir1(render.getRelativeVector(self.solid,
      panda.Vec3(0, 1, 0)))

#-------------------------------------------------------------------------------

  def move(self, period):
    command = render.getRelativeVector(self,
      panda.Vec3(self.command[0], self.command[1], 0))
    command[2] = self.command[2]
    state = render.getRelativeVector(self,
      panda.Vec3(self.state[0], self.state[1], 0))
    state[2] = self.state[2]
    
    accelerationForce = render.getRelativeVector(self,
      panda.Vec3(self.accelerationForce[0], self.accelerationForce[1], 0))
    accelerationForce[2] = self.accelerationForce[2]
    decelerationForce = render.getRelativeVector(self,
      panda.Vec3(self.decelerationForce[0], self.decelerationForce[1], 0))
    decelerationForce[2] = self.decelerationForce[2]
    
    axisForces = [0]*len(self.command)
    
    for i in range(len(command)):
      velocityError = command[i]-state[i]
      
      if abs(velocityError) > self.epsilon:
        axisForces[i] = abs(accelerationForce[i])
      else:
        axisForces[i] = abs(decelerationForce[i])
        
    self.linearJoint.axisVelocities = [state[0], state[1]]
    self.linearJoint.maxForce = axisForces[0:2]
    self.angularJoint.axisRates = [0, 0, state[2]]
    self.angularJoint.maxForce = [float("inf"), float("inf"), axisForces[2]]
    