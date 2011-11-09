from morsel.panda import *
from morsel.nodes import Sensor
from morsel.nodes.facade import Mesh
from morsel.morselc import RangeSensor as CRangeSensor

from math import pi

#-------------------------------------------------------------------------------

class RangeSensor(Sensor):
  def __init__(self, world, name, mesh, fieldOfView = [(-30, 30), (-30, 30)],
      resolution = [1.0, 1.0], rangeLimits = [0.0, 10.0], spherical = False,
      acquireColor = False, acquireLabel = None,
      cameraMaxFieldOfView = [60.0, 60.0], cameraResolution = [128, 128],
      **kargs):
    Sensor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)
    
    self.fieldOfView = fieldOfView
    self.resolution = resolution
    self.rangeLimits = rangeLimits
    self.cameraMaxFieldOfView = cameraMaxFieldOfView
    self.cameraResolution = cameraResolution
    self.spherical = spherical
    self.acquireColor = acquireColor
    if acquireLabel:
      self.acquireLabel = acquireLabel
    else:
      self.acquireLabel = ""

    self.sensor = CRangeSensor(name,
      panda.Vec2(self.fieldOfView[0][0], self.fieldOfView[1][0])*pi/180.0,
      panda.Vec2(self.fieldOfView[0][1], self.fieldOfView[1][1])*pi/180.0,
      panda.Vec2(*self.resolution)*pi/180.0,
      panda.Vec2(*self.rangeLimits),
      panda.Vec2(*self.cameraMaxFieldOfView)*pi/180,
      panda.Vec2(*self.cameraResolution),
      self.spherical, self.acquireColor, self.acquireLabel)
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
