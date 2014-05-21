from morsel.panda import *
from morsel.math import *
from morsel.control.pid import PID

#-------------------------------------------------------------------------------

class Position(PID):
  def __init__(self, target = 0, proportional_gain = 0, integral_gain = 0,
      differential_gain = 0, maxVelocity = 0, maxAcceleration = 0, **kargs):
    super(Position, self).__init__(target = [target], proportional_gain = 
      [proportional_gain], integral_gain = [integral_gain], differential_gain = 
      [differential_gain], **kargs)
      
    self.maxVelocity = maxVelocity
    self.maxAcceleration = maxAcceleration

#-------------------------------------------------------------------------------

  def getActual(self):
    return self.actuator.position
    
  actual = property(getActual)

#-------------------------------------------------------------------------------

  def setOutput(self, output):
    self.actuator.command = output
    
  output = property(None, setOutput)

#-------------------------------------------------------------------------------

  def step(self, period):
    PID.step(self, period)
