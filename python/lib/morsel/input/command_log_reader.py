from morsel.nodes import Input
from morsel.morselc import CommandLogReader as CCommandLogReader

#-------------------------------------------------------------------------------

class CommandLogReader(Input):
  def __init__(self, name, filename, actuator = None, platform = None,
      binary = True, **kargs):
    if platform:
      actuator = platform.actuator
      
    Input.__init__(self, name, **kargs)

    self.actuator = actuator
    self.filename = filename
    self.binary = binary

    self.reader = CCommandLogReader(name, self.actuator, self.filename,
      self.binary)
    self.reader.reparentTo(self)

#-------------------------------------------------------------------------------

  def inputData(self, time):
    self.reader.readData(time)
