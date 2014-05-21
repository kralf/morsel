from morsel.nodes.ode.facade import Joint
from morsel.actuators.ackermann_drive import AckermannDrive as Base
from morsel.actuators.ode.wheel_drive import WheelDrive

#-------------------------------------------------------------------------------

class AckermannDrive(WheelDrive, Base):
  def __init__(self, steeringForce = 0, **kargs):
    super(AckermannDrive, self).__init__(**kargs)
    
    if not isinstance(steeringForce, list):
      steeringForce = [steeringForce]*2
    self.steeringForce = steeringForce
    
#-------------------------------------------------------------------------------

  def move(self, period):
    for i in [0, 1]:
      self.wheelJoints[i].limits = [(self.wheelAngles[i], self.wheelAngles[i]),
                                    self.wheelJoints[i].limits[1]]
      self.wheelJoints[i].axisRates = [self.wheelSteeringRates[i],
                                       self.wheelJoints[i].axisRates[0]]
      self.wheelJoints[i].maxForce = [self.steeringForce[i],
                                      self.wheelJoints[i].maxForce[i]]
      
    WheelDrive.move(self, period)
