from morsel.actuators.linear_motor import LinearMotor as Base
from morsel.actuators.panda.motor import Motor

#-------------------------------------------------------------------------------

class LinearMotor(Motor, Base):
  def __init__(self, **kargs):
    super(LinearMotor, self).__init__(**kargs)
