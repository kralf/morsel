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
    return [(self._joint.getParamLoStop(0)*180/pi,
              self._joint.getParamHiStop(0)*180/pi),
            (self._joint.getParamLoStop(1)*180/pi,
              self._joint.getParamHiStop(1)*180/pi)]
  
  def setLimits(self, limits):
    if not isinstance(limits, list):
      limits = [limits]*2
    
    self._joint.setParamLoStop(0, limits[0][0]*pi/180)
    self._joint.setParamHiStop(0, limits[0][1]*pi/180)
    self._joint.setParamLoStop(1, limits[1][0]*pi/180)
    self._joint.setParamHiStop(1, limits[1][1]*pi/180)
  
  limits = property(getLimits, setLimits)

#-------------------------------------------------------------------------------

  def getMaxForce(self):
    return [self._joint.getParamFMax(0),
            self._joint.getParamFMax(1)]

  def setMaxForce(self, maxForce):
    if not isinstance(maxForce, list):
      maxForce = [maxForce]*2
    
    self._joint.setParamFMax(0, maxForce[0])
    self._joint.setParamFMax(1, maxForce[1])
    
  maxForce = property(getMaxForce, setMaxForce)
    
#-------------------------------------------------------------------------------

  def getFudgeFactor(self):
    return [self._joint.getParamFudgeFactor(0),
            self._joint.getParamFudgeFactor(1)]

  def setFudgeFactor(self, fudgeFactor):
    if not isinstance(fudgeFactor, list):
      fudgeFactor = [fudgeFactor]*2
    
    self._joint.setParamFudgeFactor(0, fudgeFactor[0])
    self._joint.setParamFudgeFactor(1, fudgeFactor[1])
    
  fudgeFactor = property(getFudgeFactor, setFudgeFactor)
    
#-------------------------------------------------------------------------------

  def getBouncyness(self):
    return [self._joint.getParamBounce(0),
            self._joint.getParamBounce(1)]

  def setBouncyness(self, bouncyness):
    if not isinstance(bouncyness, list):
      bouncyness = [bouncyness]*2
    
    self._joint.setParamBounce(0, bouncyness[0])
    self._joint.setParamBounce(1, bouncyness[1])
    
  bouncyness = property(getBouncyness, setBouncyness)
    
#-------------------------------------------------------------------------------

  def getCFM(self):
    return [self._joint.getParamCFM(0),
            self._joint.getParamCFM(1)]

  def setCFM(self, cfm):
    if not isinstance(cfm, list):
      cfm = [cfm]*2
    
    self._joint.setParamCFM(0, cfm[0])
    self._joint.setParamCFM(1, cfm[1])
    
  cfm = property(getCFM, setCFM)
    
#-------------------------------------------------------------------------------

  def getStopERP(self):
    return [self._joint.getParamStopERP(0),
            self._joint.getParamStopERP(1)]

  def setStopERP(self, stopERP):
    if not isinstance(stopERP, list):
      stopERP = [stopERP]*2
    
    self._joint.setParamStopERP(0, stopERP[0])
    self._joint.setParamStopERP(1, stopERP[1])
    
  stopERP = property(getStopERP, setStopERP)
    
#-------------------------------------------------------------------------------

  def getStopCFM(self):
    return [self._joint.getParamStopCFM(0),
            self._joint.getParamStopCFM(1)]

  def setStopCFM(self, stopCFM):
    if not isinstance(stopCFM, list):
      stopCFM = [stopCFM]*2
    
    self._joint.setParamStopCFM(0, stopCFM[0])
    self._joint.setParamStopCFM(1, stopCFM[1])
    
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
  