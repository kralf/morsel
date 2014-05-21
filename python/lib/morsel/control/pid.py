from morsel.panda import *
from morsel.math import *
from morsel.nodes.controller import Controller

#-------------------------------------------------------------------------------

class PID(Controller):
  def __init__(self, target = [0, 0], proportional_gain = [0, 0],
      integral_gain = [0, 0], differential_gain = [0, 0], **kargs):
    super(PID, self).__init__(**kargs)
    
    self.target = target
    
    self.proportional_gain = proportional_gain
    self.integral_gain = integral_gain
    self.differential_gain = differential_gain
    
    self.error = 0
    self.integral = 0

#-------------------------------------------------------------------------------

  def getActual(self):
    return self.actuator.state
    
  actual = property(getActual)

#-------------------------------------------------------------------------------

  def setOutput(self, output):
    self.actuator.command = output
    
  output = property(None, setOutput)

#-------------------------------------------------------------------------------

  def step(self, period):
    actual = self.actual
    output = [0]*len(actual)
    
    for i in range(min(len(actual), len(self.target))):
      error = self.target[i]-actual[i]
      self.integral += error*period
      derivative = (error-self.error)/period
      self.error = error
      
      output[i] = (self.proportional_gain*error+self.integral_gain*integral+
        self.differential_gain*derivative)
      
    self.output = output
    