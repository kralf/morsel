from morsel.panda import *
from morsel.nodes.ode.facade import Joint
from morsel.actuators.planar_motor import PlanarMotor as Base
from morsel.actuators.ode.motor import Motor

#-------------------------------------------------------------------------------

class PlanarMotor(Motor, Base):
  def __init__(self, actuated = None, **kargs):
    super(PlanarMotor, self).__init__(**kargs)

    linearLimits = [(self.minPosition[0], self.maxPosition[0]),
                    (self.minPosition[1], self.maxPosition[1]),
                    (0, 0)]
    angularLimits = [(0, 0), (0, 0), (self.minAngle, self.maxAngle)]
                   
    self.linearJoint = Joint(type = "LinearMotor", limits =
      linearLimits, stopERP = 0.9, stopCFM = 0)
    self.angularJoint = Joint(type = "AngularMotor", limits =
      angularLimits, stopERP = 0.9, stopCFM = 0, fudgeFactor = 0.1)

    self.actuated = actuated
    
#-------------------------------------------------------------------------------

  def setActuated(self, actuated):
    if self.actuated and self.actuated.body:
      self.linearJoint.detach()
      self.angularJoint.detach()
      
    super(PlanarMotor, self).setActuated(actuated)
    
    if self.actuated and self.actuated.body:
      self.linearJoint.attach(self, self.actuated)
      self.angularJoint.attach(self, self.actuated)
      
      axes = [panda.Vec3(*self.axes[0]),
              panda.Vec3(*self.axes[1]),
              panda.Vec3(0, 0, 0)]
      
      axes[0].normalize()
      axes[1].normalize()
      axes[2] = axes[0].cross(axes[1])      
      
      self.linearJoint.axes = [-axes[0], -axes[1], -axes[2]]
      self.angularJoint.mode = 1
      self.angularJoint.axes = [-axes[0], -axes[1], -axes[2]]
      
  actuated = property(Base.getActuated, setActuated)

#-------------------------------------------------------------------------------

  def move(self, period):
    Motor.move(self, period)
    
    self.linearJoint.axisVelocities = [self.linearVelocity[0],
      self.linearVelocity[1], 0]
    self.linearJoint.maxForce = [self.axisForces[0],
      self.axisForces[1], float("inf")]
      
    self.angularJoint.axisRates = [0, 0, self.angularVelocity]
    self.angularJoint.maxForce = [float("inf"), float("inf"),
      self.axisForces[2]]
