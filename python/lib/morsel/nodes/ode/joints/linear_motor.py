from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.ode.joint import Joint

#-------------------------------------------------------------------------------

class LinearMotor(Joint):
  def __init__(self, axes = [[1, 0, 0], [0, 1, 0], [0, 0, 1]], limits =
      (-float("inf"), float("inf")), maxForce = 0, fudgeFactor = 1,
      bouncyness = 0, cfm = 0, stopERP = 1, stopCFM = 0, **kargs):
    super(LinearMotor, self).__init__(type = panda.OdeLMotorJoint, **kargs)
    
    self.axes = axes
    self.limits = limits
    self.maxForce = maxForce
    self.fudgeFactor = fudgeFactor
    self.bouncyness = bouncyness
    self.cfm = cfm
    self.stopERP = stopERP
    self.stopCFM = stopCFM

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
      self._joint.setParamLoStop(i, limits[i][0])
      self._joint.setParamHiStop(i, limits[i][1])
  
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

  def setAxisVelocities(self, axisVelocities):
    if not isinstance(axisVelocities, list):
      axisVelocities = [axisVelocities]*self._joint.getNumAxes()
    
    for i in range(self._joint.getNumAxes()):
      self._joint.setParamVel(i, axisVelocities[i])
            
  axisVelocities = property(None, setAxisVelocities)

#-------------------------------------------------------------------------------

  def getAxisForces(self):
    feedback = self._joint.getFeedback()
    
    if feedback:
      axisForces = [0]*self._joint.getNumAxes()
      
      for i in range(self._joint.getNumAxes()):
        axisForces[i] = feedback.getForce1().dot(self._joint.getAxis(i))
        
      return axisForces
    else:
      return None
    
  axisForces = property(getAxisForces)
  