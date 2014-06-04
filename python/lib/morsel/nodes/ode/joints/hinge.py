from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.ode.joint import Joint

#-------------------------------------------------------------------------------

class Hinge(Joint):
  def __init__(self, anchor = [0, 0, 0], axis = [1, 0, 0], limits = 
      (-float("inf"), float("inf")), maxForce = 0, fudgeFactor = 1,
      bouncyness = 0, cfm = 0, stopERP = 1, stopCFM = 0, **kargs):
    super(Hinge, self).__init__(type = panda.OdeHingeJoint, **kargs)
    
    self.anchor = anchor
    self.axis = axis
    self.limits = limits
    self.maxForce = maxForce
    self.fudgeFactor = fudgeFactor
    self.bouncyness = bouncyness
    self.cfm = cfm
    self.stopERP = stopERP
    self.stopCFM = stopCFM

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

  def getGlobalAnchor(self):
    return self.getAnchor(render)
  
  def setGlobalAnchor(self, anchor):
    self.setAnchor(anchor, render)
  
  globalAnchor = property(getGlobalAnchor, setGlobalAnchor)
  
#-------------------------------------------------------------------------------

  def getAxis(self, node = None):
    if not node:
      node = self
    
    return node.getRelativeVector(render, self._joint.getAxis())
  
  def setAxis(self, axis, node = None):
    if not node:
      node = self
      
    self._joint.setAxis(render.getRelativeVector(node, panda.Vec3(*axis)))
  
  axis = property(getAxis, setAxis)

#-------------------------------------------------------------------------------

  def getGlobalAxis(self):
    return self.getAxis(render)
  
  def setGlobalAxis(self, axis):
    self.setAxis(axis, render)
  
  globalAxis = property(getGlobalAxis, setGlobalAxis)
  
#-------------------------------------------------------------------------------

  def getLimits(self):
    return (self._joint.getParamLoStop()*180/pi,
            self._joint.getParamHiStop()*180/pi)
  
  def setLimits(self, limits):
    self._joint.setParamLoStop(limits[0]*pi/180)
    self._joint.setParamHiStop(limits[1]*pi/180)
  
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

  def getAxisAngle(self):
    return self._joint.getAngle()*180/pi
  
  axisAngle = property(getAxisAngle)

#-------------------------------------------------------------------------------

  def getAxisRate(self):
    return self._joint.getAngleRate()*180/pi
  
  def setAxisRate(self, axisRate):
    self._joint.setParamVel(axisRate*pi/180)
            
  axisRate = property(getAxisRate, setAxisRate)

#-------------------------------------------------------------------------------

  def getAxisTorque(self):
    feedback = self._joint.getFeedback()
    
    if feedback:
      return feedback.getTorque1().dot(self._joint.getAxis())
    else:
      return None
    
  axisTorque = property(getAxisTorque)
  