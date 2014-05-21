from morsel.actuators.ackermann_drive import AckermannDrive as Base
from morsel.actuators.panda.wheel_drive import WheelDrive

#-------------------------------------------------------------------------------

class AckermannDrive(WheelDrive, Base):
  def __init__(self, **kargs):
    super(AckermannDrive, self).__init__(**kargs)
