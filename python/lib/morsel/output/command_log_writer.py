from morsel.nodes import Output
from morsel.morselc import CommandLogWriter as CCommandLogWriter

#-------------------------------------------------------------------------------

class CommandLogWriter(Output):
  def __init__(self, world, name, filename, actuator = None, platform = None,
      binary = True, logTimestamps = True, **kargs):
    if platform:
      actuator = platform.actuator
      
    Output.__init__(self, world, name, actuator, **kargs)

    self.filename = filename
    self.binary = binary
    self.logTimestamps = logTimestamps

    self.output = CCommandLogWriter(name, actuator, self.filename,
      self.binary, self.logTimestamps)
    self.output.reparentTo(self)

#-------------------------------------------------------------------------------

  def outputData(self, time):
    self.output.writeData(time)
