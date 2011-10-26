from morsel.core import *
from morsel.nodes.controller import Controller

from numpy.random import *

#-------------------------------------------------------------------------------

class Random(Controller):
  def __init__(self, world, name = "Random", range = [(0, 1), (-1, 1)],
      delay = [1, 1], **kargs):
    Controller.__init__(self, name = name, **kargs)

    self.delay = delay
    self.range = range

    self.period = [0]*len(platform.command)
    
#-------------------------------------------------------------------------------

  def updateCommand(self, period):
    command = self.platform.command

    for i in range(len(command)):
      self.period[i] += period

      if self.period[i] >= self.delay[i]:
        self.period[i] = 0
        sample = uniform(self.range[i][0], self.range[i][1])

        if sample < 0:
          command[i] = -sample*self.platform.limits[i][0]
        else:
          command[i] = sample*self.platform.limits[i][1]
      
    self.platform.command = command
