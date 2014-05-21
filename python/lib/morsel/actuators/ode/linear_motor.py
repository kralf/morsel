from morsel.nodes.ode.facade import Joint
from morsel.actuators.linear_motor import LinearMotor as Base
from morsel.actuators.ode.motor import Motor

#-------------------------------------------------------------------------------

class LinearMotor(Motor, Base):
  def __init__(self, actuated = None, **kargs):
    super(LinearMotor, self).__init__(**kargs)

    self.joint = Joint(type = "Slider", limits = (self.minPosition,
      self.maxPosition), stopERP = 0.9, stopCFM = 0)

    self.actuated = actuated
    
#-------------------------------------------------------------------------------

  def setActuated(self, actuated):
    if self.actuated and self.actuated.body:
      self.joint.detach()
      
    super(LinearMotor, self).setActuated(actuated)
    
    if self.actuated and self.actuated.body:
      self.joint.attach(self, self.actuated)
      self.joint.axis = [-self.axis[0], -self.axis[1], -self.axis[2]]
    
  actuated = property(Base.getActuated, setActuated)

#-------------------------------------------------------------------------------

  def move(self, period):
    Motor.move(self, period)
    
    self.joint.axisVelocity = self.linearVelocity
    self.joint.maxForce = self.axisForces[0]
    