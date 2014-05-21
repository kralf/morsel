from morsel.panda import *
from morsel.nodes.sensor import Sensor
from morsel.nodes.facade import Mesh
from morsel.morselc import RangeSensor as CRangeSensor

from math import pi

#-------------------------------------------------------------------------------

class RangeSensor(Sensor):
  def __init__(self, mesh = None, shader = "range_sensor.cg", fieldOfView = 
      [(-30, 30), (-30, 30)], resolution = [1.0, 1.0], rangeLimits = 
      [0.0, 10.0], spherical = False, acquireColor = False, acquireLabel = 
      None, cameraMask = 0x0000000F, cameraMaxFieldOfView = [60.0, 60.0],
      cameraResolution = [128, 128], **kargs):
    super(RangeSensor, self).__init__(**kargs)

    if mesh:
      self.mesh = Mesh(filename = mesh, flatten = True)
    
    self.shaderProgram = ShaderProgram(filename = shader)
    self.fieldOfView = fieldOfView
    self.resolution = resolution
    self.rangeLimits = rangeLimits
    self.cameraMask = cameraMask
    self.cameraMaxFieldOfView = cameraMaxFieldOfView
    self.cameraResolution = cameraResolution
    self.spherical = spherical
    self.acquireColor = acquireColor
    if acquireLabel:
      self.acquireLabel = acquireLabel
    else:
      self.acquireLabel = ""

    self.sensor = CRangeSensor("CRangeSensor", self.shaderProgram,
      panda.Vec2(self.fieldOfView[0][0], self.fieldOfView[1][0])*pi/180.0,
      panda.Vec2(self.fieldOfView[0][1], self.fieldOfView[1][1])*pi/180.0,
      panda.Vec2(*self.resolution)*pi/180.0,
      panda.Vec2(*self.rangeLimits),
      panda.Vec2(*self.cameraMaxFieldOfView)*pi/180,
      panda.Vec2(*self.cameraResolution),
      self.spherical, self.acquireColor, self.acquireLabel,
      panda.BitMask32(self.cameraMask))
    self.sensor.reparentTo(self)

    self.callback = panda.CallbackNode("Callback")
    self.callback.setDrawCallback(panda.PythonCallbackObject(self.draw))
    self.attachNewNode(self.callback)

#-------------------------------------------------------------------------------

  def showFrustums(self):
    self.sensor.showFrustums()

#-------------------------------------------------------------------------------

  def hideFrustums(self):
    self.sensor.hideFrustums()

#-------------------------------------------------------------------------------

  def draw(self, callbackData):
    if self.world:
      self.sensor.update(self.world.time, panda.Vec3(*self.globalPosition),
        panda.Vec3(*self.globalOrientation))
      
    callbackData.upcall()
