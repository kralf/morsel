from morsel.nodes.scene import Scene
from morsel.nodes.mesh import Mesh
from morsel.nodes.actuator import Actuator
from morsel.nodes.sensor import Sensor
from morsel.nodes.view import View

#-------------------------------------------------------------------------------

class World(object):
  def __init__(self, physics, period = 0.01):
    object.__init__(self)
    
    self.physics = physics
    self._scene = None

    self.meshes = []
    self.actuators = []
    self.sensors = []
    self.views = []

    self.period = period
    self.delta = 0
    self.time = 0
    
    framework.scheduler.addTask("WorldUpdate", self.update)
    
#-------------------------------------------------------------------------------

  def getScene(self):
    if self._scene:
      return self._scene
    else:
      framework.error("World has no scene")

  def setScene(self, scene):
    if not self._scene:
      self._scene = scene
    else:
      framework.error("World already has a scene")

  scene = property(getScene, setScene)

#-------------------------------------------------------------------------------

  def registerObject(self, object):
    type = object.getPythonTag("type")
    
    if issubclass(type, Scene):
      self.scene = object
    if issubclass(type, Mesh):
      self.meshes.append(object)
    if issubclass(type, Actuator):
      self.actuators.append(object)
    if issubclass(type, Sensor):
      self.sensors.append(object)
    if issubclass(type, View):
      self.views.append(object)
    
#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    pass

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    pass

#-------------------------------------------------------------------------------
  
  def update(self, time):
    self.delta += time-self.time
    update = self.delta > self.period

    while self.delta > self.period:
      self.updatePhysics(self.period)
      self.delta -= self.period

    if update:
      self.updateGraphics()

    self.time = time
    return True
