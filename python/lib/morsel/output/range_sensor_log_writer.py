from morsel.nodes.output import Output
from morsel.morselc import RangeSensorLogWriter as CRangeSensorLogWriter

#-------------------------------------------------------------------------------

class RangeSensorLogWriter(Output):
  def __init__(self, filename = None, sensor = None, binary = True, 
      logTimestamps = True, logPoses = True, logColors = False,
      logLabels = False, logInvalids = False, **kargs):
    super(RangeSensorLogWriter, self).__init__(**kargs)

    self.sensor = sensor
    self.filename = filename
    self.binary = binary
    self.logTimestamps = logTimestamps
    self.logPoses = logPoses
    self.logColors = logColors
    self.logLabels = logLabels
    self.logInvalids = logInvalids

    if self.filename and self.sensor:
      self.writer = CRangeSensorLogWriter("CRangeSensorLogWriter",
        self.sensor.sensor, self.filename, self.binary, self.logTimestamps,
        self.logPoses, self.logColors, self.logLabels, self.logInvalids)
      self.writer.reparentTo(self)
    else:
      self.writer = None

#-------------------------------------------------------------------------------

  def send(self, time):
    if self.writer:
      self.writer.writeData(time)
