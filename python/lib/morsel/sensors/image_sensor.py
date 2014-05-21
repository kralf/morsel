from morsel.panda import *
from morsel.nodes.sensor import Sensor
from morsel.nodes.facade import Mesh
from morsel.morselc import ImageSensor as CImageSensor

#-------------------------------------------------------------------------------

class ImageSensor(Sensor):
  def __init__(self, mesh = None, resolution = [640, 480],  rangeLimits = 
      [0.1, 100], filmSize = [36, 24],  focalLength = 36, cameraMask =
      0x0000000F, **kargs):
    super(ImageSensor, self).__init__(**kargs)

    if mesh:
      self.mesh = Mesh(filename = mesh, flatten = True)

    self.resolution = resolution
    self.rangeLimits = rangeLimits;
    self.filmSize = filmSize
    self.focalLength = focalLength
    self.cameraMask = cameraMask

    self.sensor = CImageSensor("CImageSensor", panda.Vec2(*self.resolution),
      panda.Vec2(*self.rangeLimits), panda.Vec2(*self.filmSize),
      self.focalLength, panda.BitMask32(self.cameraMask))
    self.sensor.reparentTo(self)

#-------------------------------------------------------------------------------

  def draw(self):
    if self.world:
      self.sensor.update(self.world.time)

#-------------------------------------------------------------------------------

  def showFrustum(self):
    self.sensor.showFrustum()

#-------------------------------------------------------------------------------

  def hideFrustum(self):
    self.sensor.hideFrustum()
