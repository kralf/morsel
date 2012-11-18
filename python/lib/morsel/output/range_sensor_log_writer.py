from morsel.nodes import Output
from morsel.morselc import RangeSensorLogWriter as CRangeSensorLogWriter

#-------------------------------------------------------------------------------

class RangeSensorLogWriter(Output):
  def __init__(self, name, filename, sensor, binary = True, 
      logTimestamps = True, logPoses = True, logColors = False,
      logLabels = False, logInvalids = False, **kargs):
    Output.__init__(self, name, **kargs)

    self.sensor = sensor
    self.filename = filename
    self.binary = binary
    self.logTimestamps = logTimestamps
    self.logPoses = logPoses
    self.logColors = logColors
    self.logLabels = logLabels
    self.logInvalids = logInvalids

    self.writer = CRangeSensorLogWriter(name, self.sensor.sensor,
      self.filename, self.binary, self.logTimestamps, self.logPoses,
      self.logColors, self.logLabels, self.logInvalids)
    self.writer.reparentTo(self)

#-------------------------------------------------------------------------------

  def outputData(self, time):
    self.writer.writeData(time)
