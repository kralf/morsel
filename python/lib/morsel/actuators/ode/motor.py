from morsel.nodes.ode.facade import Solid, Body
from morsel.actuators.motor import Motor as Base
from morsel.nodes.ode.actuator import Actuator

#-------------------------------------------------------------------------------

class Motor(Actuator, Base):
  def __init__(self, solid = None, body = None, mass = 1,
      accelerationForce = [], decelerationForce = [],
      epsilon = 1e-6, **kargs):
    super(Motor, self).__init__(**kargs)        

    self.solid = Solid(type = solid)
    self.body = Body(type = body, mass = mass)

    self.accelerationForce = accelerationForce
    self.decelerationForce = decelerationForce
    self.epsilon = epsilon
    
    self.axisForces = [0]*len(self.limits)

#-------------------------------------------------------------------------------

  def getAccelerationForce(self):
    return self._accelerationForce

  def setAccelerationForce(self, accelerationForce):
    if not isinstance(accelerationForce, list):
      self._accelerationForce = [accelerationForce]*len(self.limits)
    else:
      self._accelerationForce = accelerationForce

  accelerationForce = property(getAccelerationForce, setAccelerationForce)

#-------------------------------------------------------------------------------

  def getDecelerationForce(self):
    return self._decelerationForce

  def setDecelerationForce(self, decelerationForce):
    if not isinstance(decelerationForce, list):
      self._decelerationForce = [decelerationForce]*len(self.limits)
    else:
      self._decelerationForce = decelerationForce

  decelerationForce = property(getDecelerationForce, setDecelerationForce)

#-------------------------------------------------------------------------------

  def move(self, period):
    axisForces = [0]*len(self.limits)
    
    for i in range(len(self.limits)):
      velocityError = self.command[i]-self.state[i]
      
      if abs(velocityError) > self.epsilon:
        axisForces[i] = self.accelerationForce[i]
      else:
        axisForces[i] = self.decelerationForce[i]
    
    self.axisForces = axisForces
    