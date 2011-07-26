from morsel.core import *
from morsel.world.globals import *
from morsel.platforms.ackermann import Ackermann as Base
from morsel.nodes.facade import Mesh, Solid

#-------------------------------------------------------------------------------

class Ackermann(Base):
  def __init__(self, world, name, mesh, chassisSolid = None, wheelSolid = None,
      chassisBody = None, wheelBody = None, chassisMass = 0, wheelMass = 0,
      steeringForce = 0, propulsionForce = 0, brakingForce = 0, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)
    
    self.steeringForce = steeringForce
    self.propulsionForce = propulsionForce
    self.brakingForce = brakingForce

    self.chassisSolid = Solid(name+"ChassisSolid", chassisSolid, self.chassis,
      body = chassisBody, mass = chassisMass, parent = self)

    self.wheelSolids = []
    self.wheelJoints = []
    for wheel in self.wheels:
      solid = Solid(name+"WheelSolid", wheelSolid, wheel, body = wheelBody,
        mass = wheelMass, parent = self)
        
      joint = panda.OdeHinge2Joint(world.world)
      joint.attach(self.chassisSolid.body.body, solid.body.body)
      anchor = solid.geometry.getPos(self.world.scene)
      joint.setAnchor(anchor[0], anchor[1], anchor[2])
      joint.setAxis1(0, 0, 1)
      joint.setAxis2(0, -1, 0)
      joint.setParamFMax(0, self.steeringForce)
      joint.setParamFMax(1, self.propulsionForce)
      joint.setParamSuspensionERP(0, self.getERP(chassisMass, 0.5, 1))
      joint.setParamSuspensionCFM(0, self.getCFM(chassisMass, 0.5, 1))

      if self.isFrontWheel(wheel):
        joint.setParamLoStop(0, -self.maxSteeringAngle*pi/180)
        joint.setParamHiStop(0, self.maxSteeringAngle*pi/180)
      else:
        joint.setParamLoStop(0, 0)
        joint.setParamHiStop(0, 0)
    
      self.wheelSolids.append(solid)
      self.wheelJoints.append(joint)

    self.collider.setCollisionMasks(PLATFORM_COLLISIONS_FROM,
      PLATFORM_COLLISIONS_INTO)
    
#-------------------------------------------------------------------------------

  def getWheelAngles(self, angle):
    if tan(angle) == 0:
      return (0, 0)
      
    coti = 1 / tan(angle) + self.wheelDistance / (2 * self.axesDistance)
    coto = coti - self.wheelDistance / self.axesDistance
    i = atan(1 / coti)
    o = atan(1 / coto)
    
    return o, i

#-------------------------------------------------------------------------------

  #def setPos(self, x, y, z):
    #wpos = []
    #for w in self.wheels:
      #p = self.getRelativePoint(render, w["node"].getPos())
      #wpos.append((w, p))
    #NodePath.setPos(self, x, y, z)
    #p = render.getRelativePoint(self, self.bodyNode.getPos())
    #self.body.setPosition(x, y, z)
    
    #NodePath.setPos(self, x, y, z)
    #self.body.setPosition(self.getPos())

    #for w in wpos:
      #p = render.getRelativePoint(self, w[1])
      #w[0]["node"].setPos(p)
      #w[0]["body"].setPosition(p)

#-------------------------------------------------------------------------------

  #def setHpr(self, h, p, r):
    #wpos = []
    #for w in self.wheels:
      #p = self.getRelativePoint(render, w["node"].getPos())
      #wpos.append((w, p))
    #NodePath.setHpr(self, h, p, r)
    #self.body.setQuaternion(self.getQuat())
    
    #NodePath.setHpr(self, h, p, r)
    #self.body.setQuaternion(self.getQuat())

    #for w in wpos:
      #p = render.getRelativePoint(self, w[1])
      #w[0]["node"].setPos(p)
      #w[0]["node"].setQuat(self.getQuat())
      #w[0]["body"].setPosition(p)
      #w[0]["body"].setQuaternion(self.getQuat())

#-------------------------------------------------------------------------------
  
  #def updatePhysics(self, period):
    #currentLeft  = self.wheels[0]["joint"].getAngle1()
    #currentRight = self.wheels[1]["joint"].getAngle1()
    #nominalLeft, nominalRight = self.wheelAngles(self.command[1] * pi / 180)
    #nominalLeft =  -nominalLeft
    #nominalRight = -nominalRight
    
    #cvl = self.wheels[0]["joint"].getParamVel(0)
    #cvr = self.wheels[1]["joint"].getParamVel(0)
    #nvl = (nominalLeft  - currentLeft) / period
    #nvr = (nominalRight - currentRight) / period
    
    #self.wheels[0]["joint"].setParamVel(0, nvl)
    #self.wheels[1]["joint"].setParamVel(0, nvr)
    
    #for w in self.wheels:
      #if abs(self.command[0]) > 0.001:
        #w["joint"].setParamFMax(1, self.propulsionForce)
      #else:
        #w["joint"].setParamFMax(1, self.brakingForce)
      #angularVelocity = self.command[0] / self.wheelRadius
      #w["joint"].setParamVel(1, angularVelocity)
      
#-------------------------------------------------------------------------------
  
  #def updateGraphics(self):
    #updateFromBody(self, self.body)
    #p = self.getRelativePoint(self.bodyNode, panda.VBase3(0, 0, 0))
    #p = render.getRelativePoint(self, -p)
    #panda.NodePath.setPos(self, p)
    
    #for w in self.wheels:
      #updatePosFromBody(w["node"], w["body"])
      #p = self.getRelativePoint(render, w["node"].getPos())
