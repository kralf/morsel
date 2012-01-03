import os, string

#-------------------------------------------------------------------------------

class Pipe(object):
  def __init__(self):
    object.__init__(self)
    self.reset()

#-------------------------------------------------------------------------------

  def reset(self):
    self.out = []

#-------------------------------------------------------------------------------

  def write(self, line):
    self.out.append(line)

#-------------------------------------------------------------------------------

  def flush(self):
    output = string.join(self.out).rstrip()
    self.reset()
    
    return output
    