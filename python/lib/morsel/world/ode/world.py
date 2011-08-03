from morsel.core import *
from morsel.world import World as Base

import morsel.nodes
import morsel.nodes.simple

#-------------------------------------------------------------------------------

class World(Base):
  def __init__(self, period = 0.01, gravity = -9.81, quickStep = False):
    Base.__init__(self, "ode")

    self.period = period
    self.gravity = gravity
    self.quickStep = quickStep
    
    self.delta = 0
    self.lastTime = 0
    self.world = None
    
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

    scheduler.addTask("WorldUpdater", self.update)
  
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
  
  def update(self, time):
    self.delta += time - self.lastTime
    update = self.delta > self.period
    
    while self.delta > self.period:
      contactPoints = self.space.autoCollide()
      for actor in self.scene.actors:
        actor.updatePhysics(self.period)
      for platform in self.scene.platforms:
        platform.updatePhysics(self.period)
      if self.quickStep:
        self.world.quickStep(self.period)
      else:
        self.world.step(self.period)
      self.collisionGroup.empty()
      self.delta -= self.period
      
    if update:
      for solid in self.scene.solids:
        solid.update()
        
    self.lastTime = time
    return True
