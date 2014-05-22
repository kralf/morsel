from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.ode.joint import Joint

#-------------------------------------------------------------------------------

class Hinge2(Joint):
  def __init__(self, anchor = [0, 0, 0], axes = [[1, 0, 0], [0, 1, 0]],
      limits = (-float("inf"), float("inf")), maxForce = 0, fudgeFactor = 1,
      bouncyness = 0, cfm = 0, stopERP = 1, stopCFM = 0, suspensionERP = 1,
      suspensionCFM = 0, **kargs):
    super(Hinge2, self).__init__(type = panda.OdeHinge2Joint, **kargs)
    
    self.anchor = anchor
    self.axes = axes
    self.limits = limits
    self.maxForce = maxForce
    self.fudgeFactor = fudgeFactor
    self.bouncyness = bouncyness
    self.cfm = cfm
    self.stopERP = stopERP
    self.stopCFM = stopCFM
    self.suspensionERP = suspensionERP
    self.suspensionCFM = suspensionCFM

#-------------------------------------------------------------------------------

  def getAnchor(self, node = None):
    if not node:
      node = self
      
    anchor = node.getRelativePoint(render, panda.Point3(
      self._joint.getAnchor()))
    
    return [anchor[0], anchor[1], anchor[2]]
  
  def setAnchor(self, anchor, node = None):
    if not node:
      node = self

    self._joint.setAnchor(render.getRelativePoint(node,
      panda.Point3(*anchor)))
  
  anchor = property(getAnchor, setAnchor)

#-------------------------------------------------------------------------------

  def getAxes(self, node = None):
    if not node:
      node = self
    
    axes = [node.getRelativeVector(render, self._joint.getAxis1()),
            node.getRelativeVector(render, self._joint.getAxis2())]
      
    return [[axes[0][0], axes[0][1], axes[0][2]],
            [axes[1][0], axes[1][1], axes[1][2]]]
  
  def setAxes(self, axes, node = None):
    if not node:
      node = self
      
    self._joint.setAxis1(render.getRelativeVector(node,
      panda.Vec3(*axes[0])))
    self._joint.setAxis2(render.getRelativeVector(node,
      panda.Vec3(*axes[1])))
  
  axes = property(getAxes, setAxes)

#-------------------------------------------------------------------------------

  def getLimits(self):
    limits = [(0, 0)]*2
    
    for i in range(len(limits)):
      limits[i] = (self._joint.getParamLoStop(i)*180/pi,
                   self._joint.getParamHiStop(i)*180/pi)
    
    return limits
  
  def setLimits(self, limits):
    if not isinstance(limits, list):
      limits = [limits]*2
    
    for i in range(len(limits)):
      self._joint.setParamLoStop(i, limits[i][0]*pi/180)
      self._joint.setParamHiStop(i, limits[i][1]*pi/180)
  
  limits = property(getLimits, setLimits)

#-------------------------------------------------------------------------------

  def getMaxForce(self):
    maxForce = [0]*2
    
    for i in range(len(maxForce)):
      maxForce[i] = self._joint.getParamFMax(i)
    
    return maxForce

  def setMaxForce(self, maxForce):
    if not isinstance(maxForce, list):
      maxForce = [maxForce]*2
    
    for i in range(len(maxForce)):
      self._joint.setParamFMax(i, maxForce[i])
    
  maxForce = property(getMaxForce, setMaxForce)
    
#-------------------------------------------------------------------------------

  def getFudgeFactor(self):
    fudgeFactor = [0]*2
    
    for i in range(len(fudgeFactor)):
      fudgeFactor[i] = self._joint.getParamFudgeFactor(i)
      
    return fudgeFactor

  def setFudgeFactor(self, fudgeFactor):
    if not isinstance(fudgeFactor, list):
      fudgeFactor = [fudgeFactor]*2
    
    for i in range(len(fudgeFactor)):
      self._joint.setParamFudgeFactor(i, fudgeFactor[i])
    
  fudgeFactor = property(getFudgeFactor, setFudgeFactor)
    
#-------------------------------------------------------------------------------

  def getBouncyness(self):
    bouncyness = [0]*2
    
    for i in range(len(bouncyness)):
      bouncyness[i] = self._joint.getParamBounce(i)
      
    return bouncyness

  def setBouncyness(self, bouncyness):
    if not isinstance(bouncyness, list):
      bouncyness = [bouncyness]*2
    
    for i in range(len(bouncyness)):
      self._joint.setParamBounce(i, bouncyness[i])
    
  bouncyness = property(getBouncyness, setBouncyness)
    
#-------------------------------------------------------------------------------

  def getCFM(self):
    cfm = [0]*2
    
    for i in range(len(cfm)):
      cfm[i] = self._joint.getParamCFM(i)

    return cfm
      
  def setCFM(self, cfm):
    if not isinstance(cfm, list):
      cfm = [cfm]*2
    
    for i in range(len(cfm)):
      self._joint.setParamCFM(i, cfm[i])
    
  cfm = property(getCFM, setCFM)
    
#-------------------------------------------------------------------------------

  def getStopERP(self):
    stopERP = [0]*2
    
    for i in range(len(stopERP)):
      stopERP[i] = self._joint.getParamStopERP(i)
      
    return stopERP

  def setStopERP(self, stopERP):
    if not isinstance(stopERP, list):
      stopERP = [stopERP]*2
    
    for i in range(len(stopERP)):
      self._joint.setParamStopERP(i, stopERP[i])
    
  stopERP = property(getStopERP, setStopERP)
    
#-------------------------------------------------------------------------------

  def getStopCFM(self):
    stopCFM = [0]*2
    
    for i in range(len(stopCFM)):
      stopCFM[i] = self._joint.getParamStopCFM(i)
      
    return stopCFM

  def setStopCFM(self, stopCFM):
    if not isinstance(stopCFM, list):
      stopCFM = [stopCFM]*2
    
    for i in range(len(stopCFM)):
      self._joint.setParamStopCFM(i, stopCFM[i])
    
  stopCFM = property(getStopCFM, setStopCFM)
    
#-------------------------------------------------------------------------------

  def getSuspensionERP(self):
    return self._joint.getParamSuspensionERP(0)

  def setSuspensionERP(self, suspensionERP):
    self._joint.setParamSuspensionERP(0, suspensionERP)
    
  suspensionERP = property(getSuspensionERP, setSuspensionERP)
    
#-------------------------------------------------------------------------------

  def getSuspensionCFM(self):
    return self._joint.getParamSuspensionCFM(0)

  def setSuspensionCFM(self, suspensionCFM):
    self._joint.setParamSuspensionCFM(0, suspensionCFM)
    
  suspensionCFM = property(getSuspensionCFM, setSuspensionCFM)
    
#-------------------------------------------------------------------------------

  def setSuspension(self, mass, period, damping = 1.0):
    frequency = 2*pi/period
    delta = self.world.period
    
    self.suspensionERP = delta*frequency/(delta*frequency+2*damping)
    self.suspensionCFM = self.suspensionERP/(delta*frequency**2*mass)
    
#-------------------------------------------------------------------------------

  def getAxisAngles(self):
    return [self._joint.getAngle1()*180/pi, None]
  
  axisAngles = property(getAxisAngles)

#-------------------------------------------------------------------------------

  def getAxisRates(self):
    return [self._joint.getAngle1Rate()*180/pi,
            self._joint.getAngle2Rate()*180/pi]
  
  def setAxisRates(self, axisRates):
    if not isinstance(axisRates, list):
      axisRates = [axisRates]*2
      
    self._joint.setParamVel(0, axisRates[0]*pi/180)    
    self._joint.setParamVel(1, axisRates[1]*pi/180)    
            
  axisRates = property(getAxisRates, setAxisRates)
  