from morsel.nodes import Output
from morsel.morselc import RangeSensorLogWriter as CRangeSensorLogWriter

#-------------------------------------------------------------------------------

class RangeSensorLogWriter(Output):
  def __init__(self, world, name, sensor, filename, binary = True,
      logTimestamps = True, logColors = False, logLabels = False, **kargs):
    Output.__init__(self, world, name, sensor, **kargs)

    self.filename = filename
    self.binary = binary
    self.logTimestamps = logTimestamps
    self.logColors = logColors
    self.logLabels = logLabels

    self.output = CRangeSensorLogWriter(name, self.sensor.sensor,
      self.filename, self.binary, self.logTimestamps, self.logColors,
      self.logLabels)
    self.output.reparentTo(self)

#-------------------------------------------------------------------------------

  def outputData(self, period):
    self.output.writeData(self.world.time)
