from morsel.nodes.widget import Widget

#-------------------------------------------------------------------------------

class GUI(object):
  def __init__(self):
    object.__init__(self)

    self.horizontalAnchors = {
      "Left": -1,
      "Center": 0,
      "Right": 1
    }
    self.verticalAnchors = {
      "Top": 1,
      "Center": 0,
      "Bottom": -1
    }

    self.anchors = {}
    self.widgets = []

    self.time = 0

    for (horizontal, x) in self.horizontalAnchors.iteritems():
      for (vertical, y) in self.verticalAnchors.iteritems():
        self.anchors[horizontal, vertical] = Node(
          name = horizontal+vertical+"Anchor", position = [x, 0, y],
          parent = aspect2d)

    framework.eventManager.addEventHandler("aspectRatioChanged",
      self.updateAnchors)
    framework.scheduler.addTask("GUIUpdate", self.update)

#-------------------------------------------------------------------------------

  def getWidth(self):
    properties = framework.window.getProperties()
    return float(properties.getXSize())

  width = property(getWidth)

#-------------------------------------------------------------------------------

  def getHeight(self):
    properties = framework.window.getProperties()
    return float(properties.getYSize())

  height = property(getHeight)

#-------------------------------------------------------------------------------

  def getAspectRatio(self):
    return self.width/self.height

  aspectRatio = property(getAspectRatio)

#-------------------------------------------------------------------------------

  def registerWidget(self, widget):
    type = widget.getPythonTag("type")

    if issubclass(type, Widget):
      self.widgets.append(widget)

#-------------------------------------------------------------------------------

  def updateAnchors(self):
    aspectRatio = self.aspectRatio

    for (horizontal, x) in self.horizontalAnchors.iteritems():
      for (vertical, y) in self.verticalAnchors.iteritems():
        anchor = self.anchors[horizontal, vertical]
        if aspectRatio > 1:
          anchor.position = [x*aspectRatio, 0, y]
        else:
          anchor.position = [x, 0, y/aspectRatio]

#-------------------------------------------------------------------------------

  def update(self, time):
    for widget in self.widgets:
      if not widget.hidden:
        widget.update()

    self.time = time
    return True
