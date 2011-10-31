from morsel.core import *
from morsel.world import World as Base
from morsel.nodes.solid import Solid

#-------------------------------------------------------------------------------

class World(Base):
  def __init__(self, period = 0.01, gravity = -9.81, quickStep = False):
    Base.__init__(self, "ode")

    self.period = period
    self.gravity = gravity
    self.quickStep = quickStep
    
    self.solids = []

    self.world = panda.OdeWorld()
    self.world.setGravity(0, 0, self.gravity)
    self.world.initSurfaceTable(1)
    self.world.setContactSurfaceLayer(0.001)
    self.world.setSurfaceEntry(0, 0, mu = 100, bounce = 0.3, bounce_vel = 0.1,
      soft_erp = 0.8, soft_cfm = 1e-10, slip = 0.1, dampen = 0.002)

    self.space = panda.OdeSimpleSpace()
    self.space.setAutoCollideWorld(self.world)
    self.space.enable()
    self.collisionGroup = panda.OdeJointGroup()
    self.space.setAutoCollideJointGroup(self.collisionGroup)
  
#-------------------------------------------------------------------------------

  def getERP(self, mass, period, damping):
    frequency = 2*pi/period
    delta = self.period

    return delta*frequency/(delta*frequency+2*damping)

#-------------------------------------------------------------------------------

  def getCFM(self, mass, period, damping):
    frequency = 2*pi/period
    delta = self.period

    return self.getERP(mass, period, damping)/(delta*frequency**2*mass)

#-------------------------------------------------------------------------------

  def registerNode(self, node):
    type = node.getPythonTag("type")

    if issubclass(type, Solid):
      self.solids.append(node)

    Base.registerNode(self, node)
      
#-------------------------------------------------------------------------------
  
  def updatePhysics(self, period):
    contactPoints = self.space.autoCollide()
    for actuator in self.actuators:
      actuator.updatePhysics(self.period)
    for sensor in self.sensors:
      sensor.updatePhysics(self.period)
    if self.quickStep:
      self.world.quickStep(self.period)
    else:
      self.world.step(self.period)
    self.collisionGroup.empty()
      
#-------------------------------------------------------------------------------

  def updateGraphics(self):
    for actuator in self.actuators:
      actuator.updateGraphics()
    for solid in self.solids:
      solid.update()
    for sensor in self.sensors:
      sensor.updateGraphics()
    for view in self.views:
      view.update()
