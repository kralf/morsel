from label import Label

#-------------------------------------------------------------------------------

class FramerateDisplay(Label):
  def __init__(self, gui, name = "FramerateDisplay", period = 1.0,
      anchor = ["Right", "Top"], origin = [1, 1], frame = [0.415, 0.075],
      position = [0, -0.025], **kargs):
        
    Label.__init__(self, gui, name, text = "Framerate: n/a", anchor = anchor,
      origin = origin, frame = frame, position = position, **kargs)

    self.period = period
    self.lastTime = 0

#-------------------------------------------------------------------------------

  def update(self):
    if not self.lastTime or self.gui.time-self.lastTime >= self.period:
      self.text = ("Framerate: %.1f fps" %
        framework.scheduler.clock.getAverageFrameRate())
      self.lastTime = self.gui.time
  