from morsel.panda import *
from morsel.math import *
from morsel.nodes.ode.object import Object
from morsel.nodes.geometry import Geometry

#-------------------------------------------------------------------------------

class Body(Geometry):
  def __init__(self, name = "Body", mass = 1, centerOfMass = [0, 0, 0],
      massOffset = [0, 0, 0], **kargs):
    self._solid = None
    self._mesh = None
    
    super(Body, self).__init__(name = name, **kargs)

    self._body = panda.OdeBody(self.world._world)
    
    self.mass = mass
    self.centerOfMass = centerOfMass
    self.massOffset = massOffset
    
    self.hide(panda.BitMask32.allOn())

#-------------------------------------------------------------------------------

  def getObject(self):
    if isinstance(self.parent, Object):
      return self.parent
    else:
      return None

  def setObject(self, object):
    if self.parent != object:
      self.parent = object
      
    if self.solid and self.solid._geometry:
      self.solid._geometry.setBody(self._body)
        
    self.fit(object)
      
    self._body.setPosition(*self.globalPosition)
    self._body.setQuaternion(self.globalQuaternion)
      
  object = property(getObject, setObject)

#-------------------------------------------------------------------------------

  def getSolid(self):
    if self.object:
      return self.object.solid
    else:
      return None
    
  solid = property(getSolid)

#-------------------------------------------------------------------------------

  def getMass(self):
    return self._body.getMass().getMagnitude()
    
  def setMass(self, mass):
    _mass = self._body.getMass()
    _mass.adjust(mass)
    self._body.setMass(_mass)
    
  mass = property(getMass, setMass)
  
#-------------------------------------------------------------------------------

  def getCenterOfMass(self, node = None):
    if node:
      centerOfMass = node.getRelativePoint(self,
        self._body.getMass()._mass.getCenter())
    else:
      centerOfMass = self._body.getMass().getCenter()
    
    return [centerOfMass[0], centerOfMass[1], centerOfMass[2]]
    
  def setCenterOfMass(self, centerOfMass, node = None):
    if node:
      centerOfMass = self.getRelativePoint(node, panda.Vec3(*centerOfMass))
    else:
      centerOfMass = panda.Vec3(*centerOfMass)
    
    mass = self._body.getMass()
    mass.setParameters(mass.getMagnitude(), centerOfMass,
      mass.getInertialTensor())
    self._body.setMass(mass)
    
  centerOfMass = property(getCenterOfMass, setCenterOfMass)
  
#-------------------------------------------------------------------------------

  def getGlobalCenterOfMass(self):
    return self.getCenterOfMass(render)

  def setGlobalCenterOfMass(self, centerOfMass):
    self.setCenterOfMass(centerOfMass, render)
    
  globalCenterOfMass = property(getGlobalCenterOfMass, setGlobalCenterOfMass)
    
#-------------------------------------------------------------------------------

  def getInertialTensor(self):
    I = self._body.getMass().getInertialTensor()
    
    return [[I(0, 0), I(0, 1), I(0, 2)],
            [I(1, 0), I(1, 1), I(1, 2)],
            [I(2, 0), I(2, 1), I(2, 2)]]
    
  def setInertialTensor(self, I):
    I = panda.Mat3(I[0][0], I[0][1], I[0][2],
                   I[1][0], I[1][1], I[1][2],
                   I[2][0], I[2][1], I[2][2])
                   
    mass = self._body.getMass()
    mass.setParameters(mass.getMagnitude(), mass.getCenter(), I)    
    self._body.setMass(mass)
    
  inertialTensor = property(getInertialTensor, setInertialTensor)
  
#-------------------------------------------------------------------------------

  def setForce(self, force, node = None):
    if not node:
      node = self
      
    self._body.setForce(render.getRelativeVector(node, panda.Vec3(*force)))
    
  force = property(None, setForce)

#-------------------------------------------------------------------------------

  def setGlobalForce(self, force):
    self.setForce(force, render)
    
  globalForce = property(None, setGlobalForce)
  
#-------------------------------------------------------------------------------

  def setTorque(self, torque, node = None):
    if not node:
      node = self
    
    self._body.setTorque(render.getRelativeVector(node, panda.Vec3(*torque)))
    
  torque = property(None, setTorque)

#-------------------------------------------------------------------------------

  def setGlobalTorque(self, torque):
    self.setTorque(torque, render)
    
  globalTorque = property(None, setGlobalTorque)
  
#-------------------------------------------------------------------------------

  def getLinearVelocity(self, node = None):
    if not node:
      node = self
    
    v = self._body.getLinearVel()
    
    if node != self:
      if isinstance(node, Body):
        v -= node._body.getLinearVel()+node._body.getAngularVel().cross(
          node._body.getPosition()-self._body.getPosition())
      
      v = render.getQuat(node).xform(v)
      
    return [v[0], v[1], v[2]]
      
  def setLinearVelocity(self, linearVelocity, node = None):
    if not node:
      node = self

    v = render.getQuat(node).xform(panda.Vec3(*linearVelocity))
      
    if node != self:
      if isinstance(node, Body):
        v += node._body.getLinearVel()+node._body.getAngularVel().cross(
          node._body.getPosition()-self._body.getPosition())
        
    self._body.setLinearVel(v)
    
  linearVelocity = property(getLinearVelocity, setLinearVelocity)
      
#-------------------------------------------------------------------------------

  def getGlobalLinearVelocity(self):
    return self.getLinearVelocity(render)
    
  def setGlobalLinearVelocity(self, linearVelocity):
    self.setLinearVelocity(linearVelocity, render)
    
  globalLinearVelocity = property(getGlobalLinearVelocity,
    setGlobalLinearVelocity)

#-------------------------------------------------------------------------------

  def getAngularVelocity(self, node = None):
    if not node:
      node = self
      
    omega = self._body.getAngularVel()
    
    if node != self:
      if isinstance(node, Body):
        omega -= node._body.getAngularVel()
      
      omega = render.getQuat(node).xform(omega)
      
    return [omega[2]*180.0/pi, omega[1]*180.0/pi, omega[0]*180.0/pi]
    
  def setAngularVelocity(self, angularVelocity, node = None):
    if not node:
      node = self
      
    omega = render.getQuat(node).xform(panda.Vec3(angularVelocity[2],
      angularVelocity[1], angularVelocity[0]))
    
    if node != self:
      if isinstance(node, Body):
        omega += node._body.getAngularVel()
        
    self._body.setAngularVel(omega)

  angularVelocity = property(getAngularVelocity, setAngularVelocity)
      
#-------------------------------------------------------------------------------

  def getGlobalAngularVelocity(self):
    return self.getAngularVelocity(render)
    
  def setGlobalAngularVelocity(self, angularVelocity):
    self.setAngularVelocity(angularVelocity, render)
    
  globalAngularVelocity = property(getGlobalAngularVelocity,
    setGlobalAngularVelocity)

#-------------------------------------------------------------------------------

  def show(self, cameraMask = None):
    mesh = self.mesh
    
    if mesh:
      mesh.color = [0, 1, 0, 0.5]
      mesh.setTextureOff(1)
      mesh.setTransparency(panda.TransparencyAttrib.MAlpha)
    
    if cameraMask != None:
      Geometry.show(self, cameraMask)
    else:
      Geometry.show(self)
      
#-------------------------------------------------------------------------------

  def fit(self, node):
    super(Body, self).fit(node)
    
    position = panda.Vec3(*self.position)+panda.Vec3(*self.massOffset)
    
    self.position = [position[0], position[1], position[2]]
    
#-------------------------------------------------------------------------------

  def step(self, period):
    q_wb = panda.Quat(self._body.getQuaternion())
    T_wb = panda.TransformState.makePos(self._body.getPosition()).compose(
      panda.TransformState.makeQuat(q_wb))
    T_ob = panda.TransformState.makePos(self.getPos(self.object)).compose(
      panda.TransformState.makeQuat(self.getQuat(self.object)))
    T_wo = T_wb.compose(T_ob.getInverse())
      
    panda.NodePath.setTransform(self.object, render, T_wo)
    
#-------------------------------------------------------------------------------

  def onTranslate(self, translation):
    if self.solid and self.solid._geometry and self.solid.placeable:
      self.solid._geometry.setOffsetPosition(
        self.solid.getPos(render)-self.getPos(render))
      
#-------------------------------------------------------------------------------

  def onRotate(self, rotation):
    if self.solid and self.solid._geometry and self.solid.placeable:
      self.solid._geometry.setOffsetQuaternion(
        self.solid.getQuat(render)*self.getQuat(render).conjugate())
  