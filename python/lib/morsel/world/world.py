from morsel.nodes.scene import Scene
from morsel.nodes.actuator import Actuator
from morsel.nodes.sensor import Sensor
from morsel.nodes.view import View

#-------------------------------------------------------------------------------

class World(object):
  def __init__(self, physics, period = 0.01):
    object.__init__(self)
    
    self.physics = physics
    self.scene = None

    self.actuators = []
    self.sensors = []
    self.views = []

    self.period = period
    self.delta = 0
    self.time = 0
    
    framework.scheduler.addTask("WorldUpdate", self.update)
    
#-------------------------------------------------------------------------------

  def registerNode(self, node):
    type = node.getPythonTag("type")
    
    if issubclass(type, Actuator):
      self.actuators.append(node)
    if issubclass(type, Sensor):
      self.sensors.append(node)
    if issubclass(type, View):
      self.views.append(node)
    
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
