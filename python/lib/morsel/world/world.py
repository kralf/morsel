from morsel.nodes.scene import Scene
from morsel.nodes.actuator import Actuator
from morsel.nodes.sensor import Sensor
from morsel.nodes.animation import Animation
from morsel.nodes.view import View

#-------------------------------------------------------------------------------

class World(object):
  def __init__(self, physics = None, period = 0.01, **kargs):
    super(World, self).__init__()
    
    self.physics = physics
    self._scene = None
    self._singleStep = False

    self.actuators = []
    self.sensors = []
    self.animations = []
    self.views = []

    self.period = period
    self.delta = 0
    self.time = 0
    
    framework.addShortcut("control-s", self.singleStep,
      "Single-step the world simulation")
      
    framework.scheduler.addTask("World/Update", self.update)
    
#-------------------------------------------------------------------------------

  def getScene(self):
    return self._scene

  def setScene(self, scene):
    if not self._scene:
      self._scene = scene
    else:
      framework.error("World already has a scene.")

  scene = property(getScene, setScene)

#-------------------------------------------------------------------------------

  def addSensor(self, sensor):
    self.sensors.append(sensor)
    
#-------------------------------------------------------------------------------

  def addActuator(self, actuator):
    self.actuators.append(actuator)
    
#-------------------------------------------------------------------------------

  def addAnimation(self, animation):
    self.animations.append(animation)
    
#-------------------------------------------------------------------------------

  def addView(self, view):
    self.views.append(view)
    
#-------------------------------------------------------------------------------

  def singleStep(self):
    self._singleStep = True
    framework.scheduler.pause = False

#-------------------------------------------------------------------------------

  def step(self, period):
    for actuator in self.actuators:
      actuator.step(period)
    for sensor in self.sensors:
      sensor.step(period)      

#-------------------------------------------------------------------------------

  def draw(self):
    for animation in self.animations:
      animation.draw()
    for view in self.views:
      view.draw()

#-------------------------------------------------------------------------------
  
  def update(self, time):
    self.delta += time-self.time
    
    if not self._singleStep:
      draw = self.delta > self.period

      while self.delta > self.period:
        self.step(self.period)
        self.delta -= self.period

      self.time = time-self.delta
      
      if draw:
        self.draw()
    else:
      self._singleStep = False
      
      self.step(self.period)
      self.time = time
      self.draw()
      
      framework.scheduler.pause = True

    return True
    