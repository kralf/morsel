from morsel.nodes.input import Input
from morsel.morselc import CommandLogReader as CCommandLogReader

#-------------------------------------------------------------------------------

class CommandLogReader(Input):
  def __init__(self, filename = None, actuator = None, platform = None,
      binary = True, **kargs):
    if platform:
      actuator = platform.actuator
      
    super(CommandLogReader, self).__init__(**kargs)

    self.actuator = actuator
    self.filename = filename
    self.binary = binary

    if self.filename and self.actuator:
      self.reader = CCommandLogReader(self.name, self.actuator, self.filename,
        self.binary)
      self.reader.reparentTo(self)
    else:
      self.reader = None

#-------------------------------------------------------------------------------

  def receive(self, time):
    if self.reader:
      self.reader.readData(time)
