from morsel.nodes.ode.facade import Joint
from morsel.actuators.angular_motor import AngularMotor as Base
from morsel.actuators.ode.motor import Motor

#-------------------------------------------------------------------------------

class AngularMotor(Motor, Base):
  def __init__(self, actuated = None, **kargs):
    super(AngularMotor, self).__init__(**kargs)

    self.joint = Joint(type = "Hinge", limits = (self.minAngle,
      self.maxAngle), stopERP = 0.9, stopCFM = 0, fudgeFactor = 0.1)
    
    self.actuated = actuated
    
#-------------------------------------------------------------------------------

  def setActuated(self, actuated):
    if self.actuated and self.actuated.body:
      self.joint.detach()
      
    super(AngularMotor, self).setActuated(actuated)
    
    if self.actuated and self.actuated.body:
      self.joint.attach(self, self.actuated)
      self.joint.axis = [-self.axis[0], -self.axis[1], -self.axis[2]]
    
  actuated = property(Base.getActuated, setActuated)

#-------------------------------------------------------------------------------

  def move(self, period):
    Motor.move(self, period)
      
    self.joint.axisRate = self.angularVelocity
    self.joint.maxForce = self.axisForces[0]
    