from morsel.nodes import Input
from morsel.morselc import CommandLogReader as CCommandLogReader

#-------------------------------------------------------------------------------

class CommandLogReader(Input):
  def __init__(self, world, name, filename, actuator = None, platform = None,
      binary = True, **kargs):
    if platform:
      actuator = platform.actuator
      
    Input.__init__(self, world, name, actuator, **kargs)

    self.filename = filename
    self.binary = binary

    self.input = CCommandLogReader(name, actuator, self.filename, self.binary)
    self.input.reparentTo(self)

#-------------------------------------------------------------------------------

  def inputData(self, period):
    self.input.readData(self.world.time)
