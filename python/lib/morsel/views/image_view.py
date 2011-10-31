from morsel.nodes import View
from morsel.morselc import ImageView as CImageView

from morsel.panda import *

#-------------------------------------------------------------------------------

class ImageView(View):
  def __init__(self, world, name, sensor, **kargs):
    View.__init__(self, world, name, **kargs)

    self.sensor = sensor

    self.view = CImageView(name, self.sensor.sensor)

#-------------------------------------------------------------------------------

  def update(self):
    self.view.update(self.world.time)
  