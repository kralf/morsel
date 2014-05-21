from morsel.nodes.output import Output
from morsel.morselc import CommandLogWriter as CCommandLogWriter

#-------------------------------------------------------------------------------

class CommandLogWriter(Output):
  def __init__(self, filename = None, actuator = None, platform = None,
      binary = True, logTimestamps = True, **kargs):
    if platform:
      actuator = platform.actuator

    super(CommandLogWriter, self).__init__(**kargs)

    self.actuator = actuator
    self.filename = filename
    self.binary = binary
    self.logTimestamps = logTimestamps

    if self.filename and self.actuator:
      self.writer = CCommandLogWriter("CCommandLogWriter", self.actuator,
        self.filename, self.binary, self.logTimestamps)
      self.writer.reparentTo(self)
    else:
      self.writer = None      

#-------------------------------------------------------------------------------

  def send(self, time):
    if self.writer:
      self.writer.writeData(time)
