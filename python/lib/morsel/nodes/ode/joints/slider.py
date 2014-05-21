from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.ode.joint import Joint

#-------------------------------------------------------------------------------

class Slider(Joint):
  def __init__(self, axis = [1, 0, 0], limits = (-float("inf"), float("inf")),
      maxForce = 0, fudgeFactor = 1, bouncyness = 0, cfm = 0, stopERP = 1,
      stopCFM = 0, **kargs):
    super(Slider, self).__init__(type = panda.OdeSliderJoint, **kargs)
    
    self.axis = axis
    self.limits = limits
    self.maxForce = maxForce
    self.fudgeFactor = fudgeFactor
    self.bouncyness = bouncyness
    self.cfm = cfm
    self.stopERP = stopERP
    self.stopCFM = stopCFM

#-------------------------------------------------------------------------------

  def getAxis(self, node = None):
    if not node:
      node = self
    
    axis = node.getRelativeVector(render, self._joint.getAxis())
    
    return [axis[0], axis[1], axis[2]]
  
  def setAxis(self, axis, node = None):
    if not node:
      node = self
      
    self._joint.setAxis(render.getRelativeVector(node, panda.Vec3(*axis)))
  
  axis = property(getAxis, setAxis)

#-------------------------------------------------------------------------------

  def getLimits(self):
    return (self._joint.getParamLoStop(),
            self._joint.getParamHiStop())
  
  def setLimits(self, limits):
    self._joint.setParamLoStop(limits[0])
    self._joint.setParamHiStop(limits[1])
  
  limits = property(getLimits, setLimits)

#-------------------------------------------------------------------------------

  def getMaxForce(self):
    return self._joint.getParamFMax()

  def setMaxForce(self, maxForce):
    self._joint.setParamFMax(maxForce)
    
  maxForce = property(getMaxForce, setMaxForce)
    
#-------------------------------------------------------------------------------

  def getFudgeFactor(self):
    return self._joint.getParamFudgeFactor()

  def setFudgeFactor(self, fudgeFactor):
    self._joint.setParamFudgeFactor(fudgeFactor)
    
  fudgeFactor = property(getFudgeFactor, setFudgeFactor)
    
#-------------------------------------------------------------------------------

  def getBouncyness(self):
    return self._joint.getParamBounce()

  def setBouncyness(self, bouncyness):
    self._joint.setParamBounce(bouncyness)
    
  bouncyness = property(getBouncyness, setBouncyness)
    
#-------------------------------------------------------------------------------

  def getCFM(self):
    return self._joint.getParamCFM()

  def setCFM(self, cfm):
    self._joint.setParamCFM(cfm)
    
  cfm = property(getCFM, setCFM)
    
#-------------------------------------------------------------------------------

  def getStopERP(self):
    return self._joint.getParamStopERP()

  def setStopERP(self, stopERP):
    self._joint.setParamStopERP(stopERP)
    
  stopERP = property(getStopERP, setStopERP)
    
#-------------------------------------------------------------------------------

  def getStopCFM(self):
    return self._joint.getParamStopCFM()

  def setStopCFM(self, stopCFM):
    self._joint.setParamStopCFM(stopCFM)
    
  stopCFM = property(getStopCFM, setStopCFM)
    
#-------------------------------------------------------------------------------\

  def getAxisPosition(self):
    return self._joint.getPosition()
  
  axisPosition = property(getAxisPosition)

#-------------------------------------------------------------------------------

  def getAxisVelocity(self):
    return self._joint.getPositionRate()
  
  def setAxisVelocity(self, axisVelocity):
    self._joint.setParamVel(axisVelocity)
            
  axisVelocity = property(getAxisVelocity, setAxisVelocity)
  