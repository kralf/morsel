from morsel.actuators.planar_motor import PlanarMotor as Base
from morsel.actuators.panda.motor import Motor

#-------------------------------------------------------------------------------

class PlanarMotor(Motor, Base):
  def __init__(self, effectorSolid = None, **kargs):
    super(PlanarMotor, self).__init__(**kargs)
  