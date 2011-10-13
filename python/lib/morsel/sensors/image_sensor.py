from math import pi

from morsel.nodes import Sensor
from morsel.nodes.facade import Mesh
from morsel.morselc import ImageSensor as CImageSensor

#-------------------------------------------------------------------------------

class ImageSensor(Sensor):
  def __init__(self, world, name, mesh, resolution = [640, 480],
      range = [0.1, 100], filmSize = [36, 24],  focalLength = 36, **kargs):
    Sensor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)

    self.resolution = resolution
    self.range = range;
    self.filmSize = filmSize
    self.focalLength = focalLength

    self.sensor = CImageSensor(name, resolution[0], resolution[1],
      range[0], range[1], filmSize[0], filmSize[1], focalLength)
    self.sensor.reparentTo(self.mesh)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.sensor.update(self.world.time)

#-------------------------------------------------------------------------------

  def showFrustum(self):
    self.sensor.showFrustum()

#-------------------------------------------------------------------------------

  def hideFrustum(self):
    self.sensor.hideFrustum()
