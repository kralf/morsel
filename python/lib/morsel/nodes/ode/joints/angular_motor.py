from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.ode.joint import Joint

#-------------------------------------------------------------------------------

class AngularMotor(Joint):
  USER = 0
  EULER = 1
  
  def __init__(self, axes = [[1, 0, 0], [0, 1, 0], [0, 0, 1]], limits =
      (-float("inf"), float("inf")), maxForce = 0, fudgeFactor = 1,
      bouncyness = 0, cfm = 0, stopERP = 1, stopCFM = 0, mode = USER,
      **kargs):
    super(AngularMotor, self).__init__(type = panda.OdeAMotorJoint, **kargs)
    
    self.axes = axes
    self.limits = limits
    self.maxForce = maxForce
    self.fudgeFactor = fudgeFactor
    self.bouncyness = bouncyness
    self.cfm = cfm
    self.stopERP = stopERP
    self.stopCFM = stopCFM
    self.mode = mode

#-------------------------------------------------------------------------------

  def getAxes(self, node = None):
    if not node:
      node = self
    
    axes = [[0, 0, 0]]*self._joint.getNumAxes()
      
    for i in range(self._joint.getNumAxes()):
      axis = node.getRelativeVector(render, self._joint.getAxis(i))
      axes[i] = [axis[0], axis[1], axis[2]]
      
    return axes
  
  def setAxes(self, axes, node = None):
    if not node:
      node = self

    self._joint.setNumAxes(len(axes))
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setAxis(i, 0, render.getRelativeVector(
        node, panda.Vec3(*axes[i])))
  
  axes = property(getAxes, setAxes)

#-------------------------------------------------------------------------------

  def getGlobalAxes(self):
    return self.getAxes(render)

  def setGlobalAxes(self, axes):
    self.setAxes(axes, render)
    
  globalAxes = property(getGlobalAxes, setGlobalAxes)  
  
#-------------------------------------------------------------------------------

  def getLimits(self):
    limits = [(0, 0)]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      limits[i] = (self._joint.getParamLoStop(i),
                   self._joint.getParamHiStop(i))
      
    return limits
  
  def setLimits(self, limits):
    if not isinstance(limits, list):
      limits = [limits]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamLoStop(i, limits[i][0]*pi/180)
      self._joint.setParamHiStop(i, limits[i][1]*pi/180)
  
  limits = property(getLimits, setLimits)

#-------------------------------------------------------------------------------

  def getMaxForce(self):
    maxForce = [0]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      maxForce[i] = self._joint.getParamFMax(i)

    return maxForce

  def setMaxForce(self, maxForce):
    if not isinstance(maxForce, list):
      maxForce = [maxForce]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamFMax(i, maxForce[i])
    
  maxForce = property(getMaxForce, setMaxForce)
    
#-------------------------------------------------------------------------------

  def getFudgeFactor(self):
    fudgeFactor = [0]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      fudgeFactor[i] = self._joint.getParamFudgeFactor(i)

    return fudgeFactor

  def setFudgeFactor(self, fudgeFactor):
    if not isinstance(fudgeFactor, list):
      fudgeFactor = [fudgeFactor]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamFudgeFactor(i, fudgeFactor[i])
    
  fudgeFactor = property(getFudgeFactor, setFudgeFactor)
    
#-------------------------------------------------------------------------------

  def getBouncyness(self):
    bouncyness = [0]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      bouncyness[i] = self._joint.getParamBounce(i)

    return bouncyness

  def setBouncyness(self, bouncyness):
    if not isinstance(bouncyness, list):
      bouncyness = [bouncyness]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamBounce(i, bouncyness[i])
    
  bouncyness = property(getBouncyness, setBouncyness)
    
#-------------------------------------------------------------------------------

  def getCFM(self):
    cfm = [0]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      cfm[i] = self._joint.getParamCFM(i)
      
    return cfm

  def setCFM(self, cfm):
    if not isinstance(cfm, list):
      cfm = [cfm]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamCFM(i, cfm[i])
    
  cfm = property(getCFM, setCFM)
    
#-------------------------------------------------------------------------------

  def getStopERP(self):
    stopERP = [0]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      stopERP[i] = self._joint.getParamStopERP(i)
      
    return stopERP

  def setStopERP(self, stopERP):
    if not isinstance(stopERP, list):
      stopERP = [stopERP]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamStopERP(i, stopERP[i])
    
  stopERP = property(getStopERP, setStopERP)
    
#-------------------------------------------------------------------------------

  def getStopCFM(self):
    stopCFM = [0]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      stopCFM[i] = self._joint.getParamStopCFM(i)
      
    return stopCFM

  def setStopCFM(self, stopCFM):
    if not isinstance(stopCFM, list):
      stopCFM = [stopCFM]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamStopCFM(i, stopCFM[i])
    
  stopCFM = property(getStopCFM, setStopCFM)
    
#-------------------------------------------------------------------------------

  def getMode(self):
    return self._joint.getMode()

  def setMode(self, mode):
    self._joint.setMode(mode)
    
  mode = property(getMode, setMode)
    
#-------------------------------------------------------------------------------

  def getAxisAngles(self):
    axisAngles = [0]*self._joint.getNumAxes()

    for i in range(self._joint.getNumAxes()):
      axisAngles[i] = self._joint.getAngle(i)*180/pi
    
    return axisAngles
    
  def setAxisAngles(self, axisAngles):
    if not isinstance(axisAngles, list):
      axisAngles = [axisAngles]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setAngle(i, axisAngles[i]*pi/180)
  
  axisAngles = property(getAxisAngles, setAxisAngles)

#-------------------------------------------------------------------------------

  def getAxisRates(self):
    axisRates = [0]*self._joint.getNumAxes()

    for i in range(self._joint.getNumAxes()):
      axisRates[i] = self._joint.getAngleRate(i)*180/pi
    
    return axisRates
    
  def setAxisRates(self, axisRates):
    if not isinstance(axisRates, list):
      axisRates = [axisRates]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamVel(i, axisRates[i]*pi/180)
            
  axisRates = property(getAxisRates, setAxisRates)
  