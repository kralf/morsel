from morsel.nodes import Output
from morsel.morselc import RangeSensorLogWriter as CRangeSensorLogWriter

#-------------------------------------------------------------------------------

class RangeSensorLogWriter(Output):
  def __init__(self, world, name, filename, sensor, binary = True,
      logTimestamps = True, logColors = False, logLabels = False,
      logInvalids = False, **kargs):
    Output.__init__(self, world, name, **kargs)

    self.sensor = sensor
    self.filename = filename
    self.binary = binary
    self.logTimestamps = logTimestamps
    self.logColors = logColors
    self.logLabels = logLabels
    self.logInvalids = logInvalids

    self.writer = CRangeSensorLogWriter(name, self.sensor.sensor,
      self.filename, self.binary, self.logTimestamps, self.logColors,
      self.logLabels, self.logInvalids)
    self.writer.reparentTo(self)

#-------------------------------------------------------------------------------

  def outputData(self, time):
    self.writer.writeData(time)
