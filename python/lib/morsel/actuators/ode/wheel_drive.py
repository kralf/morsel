from morsel.panda import *
from morsel.nodes.ode.facade import Solid, Body, Joint
from morsel.actuators.wheel_drive import WheelDrive as Base
from morsel.actuators.ode.drive import Drive

#-------------------------------------------------------------------------------

class WheelDrive(Drive, Base):
  def __init__(self, frameSolid = None, frameBody = None, frameMass = 1,
      wheelSolids = None, wheelBodies = None, wheelMasses = 1,
      wheelSuspensions = 0, propulsionForce = 0, brakingForce = 0,
      epsilon = 1e-6, actuated = None, **kargs):
    super(WheelDrive, self).__init__(solid = frameSolid, body = frameBody,
      mass = frameMass, **kargs)

    if not isinstance(wheelSolids, list):
      wheelSolids = [wheelSolids]*len(self.wheels)      
    if not isinstance(wheelBodies, list):
      wheelBodies = [wheelBodies]*len(self.wheels)
      
    for i in range(len(self.wheels)):
      self.wheels[i].solid = Solid(type = wheelSolids[i])
      self.wheels[i].body = Body(type = wheelBodies[i])
      self.wheels[i].collisionMasks = self.collisionMasks

    self.wheelJoints = []      
    for i in range(len(self.wheels)):
      wheelAnchor = self.wheels[i].body.getPosition(self)
      joint = Joint(type = "Hinge2", objects = [self, self.wheels[i]],
        anchor = wheelAnchor, axes = [[0, 0, -1], [0, -1, 0]], limits =
        [(0, 0), (-float("inf"), float("inf"))], stopERP = 0.9, stopCFM = 0)
      self.wheelJoints.append(joint)

    self.wheelMasses = wheelMasses
    self.wheelSuspensions = wheelSuspensions
        
    if not isinstance(propulsionForce, list):
      propulsionForce = [propulsionForce]*len(self.wheels)
    if not isinstance(brakingForce, list):
      brakingForce = [brakingForce]*len(self.wheels)
      
    self.propulsionForce = propulsionForce
    self.brakingForce = brakingForce
    self.epsilon = epsilon
    
    self.actuated = actuated
    
#-------------------------------------------------------------------------------

  def getWheelMasses(self):
    wheelMasses = [0]*len(self.wheels)
    
    for i in range(len(self.wheels)):
      wheelMasses[i] = self.wheels[i].mass
    
    return wheelMasses
    
  def setWheelMasses(self, wheelMasses):
    if not isinstance(wheelMasses, list):
      wheelMasses = [wheelMasses]*len(self.wheels)
      
    for i in range(len(self.wheels)):
      self.wheels[i].body.mass = wheelMasses[i]
  
  wheelMasses = property(getWheelMasses, setWheelMasses)
  
#-------------------------------------------------------------------------------

  def getWheelSuspensions(self):
    return self._wheelSuspensions
    
  def setWheelSuspensions(self, wheelSuspensions):
    if not isinstance(wheelSuspensions, list):
      self._wheelSuspensions = [wheelSuspensions]*len(self.wheels)
    else:
      self._wheelSuspensions = wheelSuspensions

    if self.actuated and self.actuated.body:
      for i in range(len(self.wheels)):
        self.wheelJoints[i].setSuspension(self.actuated.body.mass,
          self._wheelSuspensions[i])
    
  wheelSuspensions = property(getWheelSuspensions, setWheelSuspensions)

#-------------------------------------------------------------------------------

  def setActuated(self, actuated):
    super(WheelDrive, self).setActuated(actuated)
    
    if self.actuated and self.actuated.body:
      self.wheelSuspensions = self._wheelSuspensions
    
  actuated = property(Base.getActuated, setActuated)

#-------------------------------------------------------------------------------

  def move(self, period):
    for i in range(len(self.wheels)):
      self.wheelJoints[i].axisRates = [self.wheelJoints[i].axisRates[0],
                                       self.wheelRates[i]]
      
      wheelRateError = self.wheelRates[i]-self.wheelJoints[i].axisRates[1]
      if wheelRateError > self.epsilon:
        self.wheelJoints[i].maxForce = [self.wheelJoints[i].maxForce[0],
                                        self.propulsionForce[i]]
      elif wheelRateError < -self.epsilon:
        self.wheelJoints[i].maxForce = [self.wheelJoints[i].maxForce[0],
                                        self.brakingForce[i]]
      else:
        self.wheelJoints[i].maxForce = [self.wheelJoints[i].maxForce[0], 0]
    