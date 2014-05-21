from morsel.panda import *
from morsel.nodes.ode.object import Object
from morsel.world import World as Base

from math import *

#-------------------------------------------------------------------------------

class World(Base):
  def __init__(self, period = 0.01, gravity = -9.81, friction = 100.0,
      slip = 0.1, bouncyness = 0.3, bounceVelocity = 0.1, softERP = 0.8,
      softCFM = 1e-10, dampening = 0.002, contactDepth = 0.001,
      quickStep = False, **kargs):
    self._friction = friction
    self._slip = slip
    self._bouncyness = bouncyness
    self._bounceVelocity = bounceVelocity
    self._softERP = softERP
    self._softCFM = softCFM
    self._dampening = dampening
    
    super(World, self).__init__(physics = "ode", period = period)
    
    self._world = panda.OdeWorld()
    self._world.initSurfaceTable(1)
    
    self.space = panda.OdeSimpleSpace()
    self.space.setAutoCollideWorld(self._world)
    self.space.enable()
    self.contacts = panda.OdeJointGroup()
    self.space.setAutoCollideJointGroup(self.contacts)
    
    self.gravity = gravity
    self.contactDepth = contactDepth
    self.updateSurfaceEntry()
    
    self.quickStep = quickStep
  
#-------------------------------------------------------------------------------

  def getGravity(self):
    return self._world.getGravity()

  def setGravity(self, gravity):
    self._world.setGravity(0, 0, gravity)
    
  gravity = property(getGravity, setGravity)
    
#-------------------------------------------------------------------------------

  def getFriction(self):
    return self._friction

  def setFriction(self, friction):
    self._friction = friction
    self.updateSurfaceEntry()
    
  friction = property(getFriction, setFriction)
    
#-------------------------------------------------------------------------------

  def getSlip(self):
    return self._slip

  def setSlip(self, slip):
    self._slip = slip
    self.updateSurfaceEntry()
    
  slip = property(getSlip, setSlip)
    
#-------------------------------------------------------------------------------

  def getBouncyness(self):
    return self._bouncyness

  def setBouncyness(self, bouncyness):
    self._bouncyness = max(0.0, min(1.0, bouncyness))
    self.updateSurfaceEntry()
    
  bouncyness = property(getBouncyness, setBouncyness)
    
#-------------------------------------------------------------------------------

  def getBounceVelocity(self):
    return self._bounceVelocity

  def setBounceVelocity(self, bounceVelocity):
    self._bounceVelocity = bounceVelocity
    self.updateSurfaceEntry()
    
  bounceVelocity = property(getBounceVelocity, setBounceVelocity)
    
#-------------------------------------------------------------------------------

  def getSoftERP(self):
    return self._softERP

  def setSoftERP(self, softERP):
    self._softERP = softERP
    self.updateSurfaceEntry()
    
  softERP = property(getSoftERP, setSoftERP)
    
#-------------------------------------------------------------------------------

  def getSoftCFM(self):
    return self._softCFM

  def setSoftCFM(self, softCFM):
    self._softCFM = softCFM
    self.updateSurfaceEntry()
    
  softCFM = property(getSoftCFM, setSoftCFM)
    
#-------------------------------------------------------------------------------

  def getDampening(self):
    return self._dampening

  def setDampening(self, dampening):
    self._dampening = dampening
    self.updateSurfaceEntry()
    
  dampening = property(getDampening, setDampening)
    
#-------------------------------------------------------------------------------

  def getContactDepth(self):
    return self._world.getContactSurfaceLayer()

  def setContactDepth(self, contactDepth):
    self._world.setContactSurfaceLayer(contactDepth)
    
  contactDepth = property(getContactDepth, setContactDepth)
    
#-------------------------------------------------------------------------------

  def updateSurfaceEntry(self, surface1 = 0, surface2 = 0):
    self._world.setSurfaceEntry(surface1, surface2, mu = self.friction,
      bounce = self.bouncyness, bounce_vel = self.bounceVelocity,
      soft_erp = self.softERP, soft_cfm = self.softCFM, slip = self.slip,
      dampen = self.dampening)
  
#-------------------------------------------------------------------------------
  
  def step(self, period):
    self.space.autoCollide()

    if self.quickStep:
      self._world.quickStep(period)
    else:
      self._world.step(period)
    self.contacts.empty()
    
    if self.scene:
      for body in self.scene.bodies:
        body.step(period)      
    
    Base.step(self, period)
    