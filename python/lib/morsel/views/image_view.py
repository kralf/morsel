from morsel.panda import *
from morsel.nodes.view import View
from morsel.morselc import ImageView as CImageView

#-------------------------------------------------------------------------------

class ImageView(View):
  def __init__(self, sensor = None, **kargs):
    self._sensor = None
    self.view = None

    super(ImageView, self).__init__(**kargs)
    
    self.sensor = sensor

#-------------------------------------------------------------------------------

  def getSensor(self):
    return self._sensor
    
  def setSensor(self, sensor):
    if self._sensor:
      self.view.detachNode()
      self.view = None
      self.detachNode()
      
    self._sensor = sensor
    
    if self._sensor:
      self.view = CImageView("CImageView", self.sensor.sensor)
      self.view.reparentTo(self)
      self.parent = self._sensor
      
  sensor = property(getSensor, setSensor)

#-------------------------------------------------------------------------------

  def draw(self):
    if self.view and self.world:
      self.view.update(self.world.time)
  