from label import Label

import math

#-------------------------------------------------------------------------------

class ClockDisplay(Label):
  def __init__(self, gui, name = "ClockDisplay", anchor = ["Left", "Top"],
      origin = [-1, 1], frame = [0.525, 0.075], position = [0, -0.025],
      **kargs):

    Label.__init__(self, gui, name, text = "World time: n/a", anchor = anchor,
      origin = origin, frame = frame, position = position, **kargs)

#-------------------------------------------------------------------------------

  def update(self):
    time = framework.scheduler.time
    
    hours = math.floor(time/3600)
    mins = math.floor((time-hours*3600)/60)
    secs = math.floor(time-hours*3600-mins*60)
    msecs = (time-hours*3600-mins*60-secs)*1000

    self.text = ("World time: %02d:%02d:%02d:%03d" % (hours, mins, secs, msecs))
  