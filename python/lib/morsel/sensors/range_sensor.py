from math import pi

from morsel.nodes import Sensor
from morsel.nodes.facade import Mesh
from morsel.morselc import RangeSensor as CRangeSensor

#-------------------------------------------------------------------------------

class RangeSensor(Sensor):
  def __init__(self, world, name, mesh, fieldOfView = [(-30, 30), (-30, 30)],
      resolution = [1.0, 1.0], rangeLimits = [0.0, 10.0], spherical = False,
      acquireColor = False, cameraMaxFieldOfView = [60.0, 60.0],
      cameraResolution = [128, 128], **kargs):
    Sensor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)
    
    self.fieldOfView = fieldOfView
    self.resolution = resolution
    self.rangeLimits = rangeLimits
    self.cameraMaxFieldOfView = cameraMaxFieldOfView
    self.cameraResolution = cameraResolution
    self.spherical = spherical
    self.acquireColor = acquireColor

    self.sensor = CRangeSensor("C"+name,
      self.fieldOfView[0][0]*pi/180.0, self.fieldOfView[0][1]*pi/180.0,
      self.fieldOfView[1][0]*pi/180.0, self.fieldOfView[1][1]*pi/180.0,
      self.resolution[0]*pi/180.0, self.resolution[1]*pi/180.0,
      self.rangeLimits[0], self.rangeLimits[1],
      self.cameraMaxFieldOfView[0]*pi/180.0,
      self.cameraMaxFieldOfView[1]*pi/180.0,
      self.cameraResolution[0], self.cameraResolution[1],
      self.spherical, self.acquireColor)
    self.sensor.reparentTo(self.mesh)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.sensor.update(self.world.time)

#-------------------------------------------------------------------------------

  def showFrustums(self):
    self.sensor.showFrustums()

#-------------------------------------------------------------------------------

  def hideFrustums(self):
    self.sensor.hideFrustums()
