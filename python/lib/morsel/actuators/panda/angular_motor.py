from morsel.actuators.angular_motor import AngularMotor as Base
from morsel.actuators.panda.motor import Motor

#-------------------------------------------------------------------------------

class AngularMotor(Motor, Base):
  def __init__(self, **kargs):
    super(AngularMotor, self).__init__(**kargs)
    