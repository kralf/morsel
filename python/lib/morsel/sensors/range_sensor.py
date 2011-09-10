from morsel.nodes import Sensor
from morsel.nodes.facade import Mesh
from morsel.morselc import RangeSensor as CRangeSensor

#-------------------------------------------------------------------------------

class RangeSensor(Sensor):
  def __init__(self, world, name, mesh, fieldOfView = [45.0, 45.0],
      resolution = [1.0, 1.0], rangeLimits = [0.0, 10.0], acquireColor = False,
      cameraMaxFieldOfView = [60.0, 60.0], **kargs):
    Sensor.__init__(self, world, name, **kargs)

    self.mesh = Mesh(name+"Mesh", mesh, parent = self)
    
    self.fieldOfView = fieldOfView
    self.resolution = resolution
    self.rangeLimits = rangeLimits
    self.numRanges = [int(self.fieldOfView[0]/self.resolution[0]),
      int(self.fieldOfView[1]/self.resolution[1])]
    self.acquireColor = acquireColor
    self.cameraMaxFieldOfView = cameraMaxFieldOfView

    self.sensor = CRangeSensor("C"+name, self.numRanges[0]*
      self.resolution[0], self.numRanges[1]*self.resolution[1],
      self.numRanges[0], self.numRanges[1], self.rangeLimits[0],
      self.rangeLimits[1], self.cameraMaxFieldOfView[0],
      self.cameraMaxFieldOfView[1], self.acquireColor)
    self.sensor.reparentTo(self.mesh)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    self.sensor.update(self.world.time)
