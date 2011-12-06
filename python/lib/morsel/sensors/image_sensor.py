from morsel.panda import *
from morsel.nodes import Sensor
from morsel.nodes.facade import Mesh
from morsel.morselc import ImageSensor as CImageSensor

#-------------------------------------------------------------------------------

class ImageSensor(Sensor):
  def __init__(self, world, name, mesh, resolution = [640, 480],
      rangeLimits = [0.1, 100], filmSize = [36, 24],  focalLength = 36,
      **kargs):
    Sensor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name = name+"Mesh", filename = mesh, parent = self)

    self.resolution = resolution
    self.rangeLimits = rangeLimits;
    self.filmSize = filmSize
    self.focalLength = focalLength

    self.sensor = CImageSensor(name, panda.Vec2(*resolution),
      panda.Vec2(*rangeLimits), panda.Vec2(*filmSize), focalLength)
    self.sensor.reparentTo(self)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.sensor.update(self.world.time)

#-------------------------------------------------------------------------------

  def showFrustum(self):
    self.sensor.showFrustum()

#-------------------------------------------------------------------------------

  def hideFrustum(self):
    self.sensor.hideFrustum()
