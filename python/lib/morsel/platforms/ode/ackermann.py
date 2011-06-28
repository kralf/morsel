from globals import *
from shared  import *
from morsel.core    import *
from math    import *
import time

DEBUG = False

#-------------------------------------------------------------------------------

class Ackermann( panda.NodePath ):
  def __init__( self, name, world, mesh = None, pivot = None,
                      axesDistance = None,
                      steeringForce = None, propulsionForce = None, brakingForce = None,
                      vehicleMass = None, massOffset = None, collisionOffset = None,
                      wheelMass = None, wheelRadius = None,
                      maxSpeed = None, maxSteeringAngle = None,
                      **kargs ):
    NodePath.__init__( self, name )
    self.mesh  = loadMesh( name + "Mesh", mesh )
    self.mesh.reparentTo( self )
    self.mesh.setPos( - panda.VBase3( *pivot ) )
    self.command          = [0, 0]
    self.axesDistance     = axesDistance
    self.steeringForce    = steeringForce
    self.propulsionForce  = propulsionForce
    self.brakingForce     = brakingForce
    self.vehicleMass      = vehicleMass
    self.massOffset       = massOffset
    self.wheelMass        = wheelMass
    self.wheelRadius      = wheelRadius
    self.maxSpeed         = maxSpeed
    self.maxSteeringAngle = maxSteeringAngle
    
    self.world        = world.world
    self.odeTimeDelta = world.period
    self.space        = world.space
    
    
    self.setCommand( [0, 0] )
    self.commandSize = 2
    self.commandLimits = [
      ( -maxSpeed, maxSpeed),
      ( -maxSteeringAngle, maxSteeringAngle )
    ]
    
    self.computeDistances()
    self.setupChassis()
    self.setupWheels()
    
  ##-----
    
  def computeDistances( self ):
    bounds      = self.mesh.getTightBounds() 
    self.x1     = bounds[0][0]
    self.x2     = bounds[1][0]
    self.y1     = bounds[0][1]
    self.y2     = bounds[1][1]
    self.z1     = bounds[0][2]
    self.z2     = bounds[1][2]
    
    self.lengthX = self.x2 - self.x1
    self.lengthY = self.y2 - self.y1
    self.lengthZ = self.z2 - self.z1
    self.wheelDistance    = self.lengthY - 2 * self.wheelRadius
    
  #-----
  
  def setupChassis( self ):
    self.body = panda.OdeBody( self.world )
    self.body.setPosition( 0, 0, self.massOffset )
    self.body.setQuaternion( panda.Quat( 1, 0, 0, 0 ) )

    self.mass = panda.OdeMass()
    self.mass.setBoxTotal( 
      self.vehicleMass, 
      self.axesDistance, 
      self.wheelDistance, 
      2 * self.wheelRadius )
      
    self.bodyNode = panda.NodePath( "massNode" )
    self.bodyNode.reparentTo( self )
    self.bodyNode.setPos( self.axesDistance / 2, 0, self.massOffset )

    self.geometry = panda.OdeBoxGeom(
      self.space,
      self.lengthX,
      self.lengthY, 
      self.lengthZ - self.wheelRadius )
    self.geometry.setBody( self.body )

    p = self.bodyNode.getRelativePoint( self, panda.VBase3(
      (self.x1 + self.x2 ) / 2, 
      (self.y1 + self.y2 ) / 2, 
      self.lengthZ / 2 - self.wheelRadius / 2
    ) )
    
    self.geometry.setOffsetPosition( p )
    self.geometry.setCategoryBits( CHASSIS_CATEGORY )
    self.geometry.setCollideBits( CHASSIS_COLLIDE_BITS )
    
    if DEBUG:
      centerNode = panda.NodePath( "centerNode" )
      centerNode.reparentTo( self )
      centerNode.setPos( self.axesDistance / 2, 0, 0 )
      
      mesh = loadMesh( self.getName() + "_mass", "geometry/cube.bam" )
      mesh.setScale( 
        self.axesDistance, 
        self.wheelDistance, 
        2 * self.wheelRadius )
      mesh.setColor( 1, 0, 0, 0.5 )
      mesh.setTransparency( True )
      mesh.reparentTo( centerNode )
      mesh.setPos( self.body.getPosition() )
      
      mesh = loadMesh( self.getName() + "_chassis", "geometry/cube.bam" )
      mesh.setScale( 
        self.lengthX, 
        self.lengthY, 
        self.lengthZ - self.wheelRadius )
      mesh.setColor( 0, 0, 1, 0.5 )
      mesh.setTransparency( True )
      mesh.reparentTo( centerNode )
      mesh.setPos( self.geometry.getPosition() )

  #-----
  
  def setupWheels( self ):
    self.wheels     = []
    
    x = 0
    y = 0
    z = 0
    
    for i in xrange( 4 ):
      if i % 2 == 0:
        y =  self.wheelDistance / 2
      else:
        y = -self.wheelDistance / 2
        
      if i < 2:
        x = self.axesDistance / 2
      else:
        x = -self.axesDistance / 2
        
      wgeom = panda.GeomNode( "w%i" % i )
      wnode = render.attachNewNode( wgeom )
      wgeom.setBounds( panda.BoundingSphere( panda.Point3(0, 0, 0), self.wheelRadius ) )
      wgeom.setFinal( 1 )
      wnode.setPos( x, y, z)
      
      if DEBUG:
        wnode.showBounds()
        
      
      mass = panda.OdeMass()
      mass.setSphereTotal( self.wheelMass, self.wheelRadius )
      
      body = panda.OdeBody( self.world )
      body.setMass( mass )
      body.setPosition( x, y, z )
      body.setQuaternion( panda.Quat( 1, 0, 0, 0 ) )

      geometry = panda.OdeSphereGeom( self.space, self.wheelRadius )
      geometry.setBody( body )
      geometry.setCategoryBits( ACTUATOR_CATEGORY )
      geometry.setCollideBits( ACTUATOR_COLLIDE_BITS )
      
      joint = panda.OdeHinge2Joint( self.world )
      joint.attach( self.body, body )
      joint.setAnchor( x, y, z )
      joint.setAxis1( 0,  0, 1 )
      joint.setAxis2( 0, -1, 0 )
      joint.setParamFMax( 0, self.steeringForce )
      joint.setParamFMax( 1, self.propulsionForce )
      joint.setParamSuspensionERP( 0, erp( self.vehicleMass, 0.5, 1, self.odeTimeDelta ) )
      joint.setParamSuspensionCFM( 0, cfm( self.vehicleMass, 0.5, 1, self.odeTimeDelta ) ) 
      #joint.setParamSuspensionERP( 0, erp( self.vehicleMass, 0.5, 0.05, self.odeTimeDelta ) )
      #joint.setParamSuspensionCFM( 0, cfm( self.vehicleMass, 0.5, 0.05, self.odeTimeDelta ) ) 

      front = True
      if i <= 1:
        joint.setParamLoStop( 0, -self.maxSteeringAngle * pi / 180 )
        joint.setParamHiStop( 0,  self.maxSteeringAngle * pi / 180 )
      else:
        joint.setParamLoStop( 0, 0 )
        joint.setParamHiStop( 0, 0 )
        front = False
        
      self.wheels.append( { "body": body, "geometry": geometry, "joint": joint, "node": wnode, "front": front } )

  #-----
    
  def setPos( self, position ):
    wpos = []
    for w in self.wheels:
      p = self.getRelativePoint( render, w["node"].getPos() )
      wpos.append( (w, p) )
    NodePath.setPos( self, position )
    p = render.getRelativePoint( self, self.bodyNode.getPos() )
    self.body.setPosition( position[0], position[1], position[2] )
    for w in wpos:
      p = render.getRelativePoint( self, w[1] )
      w[0]["node"].setPos( p )
      w[0]["body"].setPosition( p )

  #-----

  def setHpr( self, hpr ):
    wpos = []
    for w in self.wheels:
      p = self.getRelativePoint( render, w["node"].getPos() )
      wpos.append( (w, p) )
    NodePath.setHpr( self, hpr )
    self.body.setQuaternion( self.getQuat() )
    for w in wpos:
      p = render.getRelativePoint( self, w[1] )
      w[0]["node"].setPos( p )
      w[0]["node"].setQuat( self.getQuat() )
      w[0]["body"].setPosition( p )
      w[0]["body"].setQuaternion( self.getQuat() )
    
  #-----
  
  def getCommand( self ):
    return self.velocity, self.steeringAngle

  def setCommand( self, command ):
    self.velocity, self.steeringAngle = command

  command = property( getCommand, setCommand )
  
  #-----
  
  def wheelAngles( self, angle ):
    if tan( angle ) == 0:
      return ( 0, 0 )
    cotI = 1 / tan( angle ) + self.wheelDistance / ( 2 * self.axesDistance )
    cotO = cotI - self.wheelDistance / self.axesDistance
    i = atan( 1 / cotI )
    o = atan( 1 / cotO )
    return o, i
    
  #-----
  
  def updatePhysics( self, period ):
    currentLeft  = self.wheels[0]["joint"].getAngle1()
    currentRight = self.wheels[1]["joint"].getAngle1()
    nominalLeft, nominalRight = self.wheelAngles( self.steeringAngle * pi / 180 )
    nominalLeft =  -nominalLeft
    nominalRight = -nominalRight
    cvl = self.wheels[0]["joint"].getParamVel( 0 )
    cvr = self.wheels[1]["joint"].getParamVel( 0 )
    nvl = ( nominalLeft  - currentLeft ) / period
    nvr = ( nominalRight - currentRight ) / period
    
    self.wheels[0]["joint"].setParamVel( 0, nvl )
    self.wheels[1]["joint"].setParamVel( 0, nvr )
    
    for w in self.wheels:
      if abs( self.velocity ) > 0.001:
        w["joint"].setParamFMax( 1, self.propulsionForce )
      else:
        w["joint"].setParamFMax( 1, self.brakingForce )
      angularVelocity = self.velocity / self.wheelRadius
      w["joint"].setParamVel( 1, angularVelocity )
      
  #-----
  
  def updateGraphics( self ):
    #print self.getPos()
    if DEBUG:
      try:
        newTime = time.time()
        newPos  = self.getPos()
        delta    = newTime - self.oldTime
        a = self.oldPos
        b = newPos
        distance = sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2  )
        self.oldTime = newTime
        self.oldPos  = newPos
        print "Velocity:", ( distance / 1000 ) / ( delta / 3600 ), delta
      except Exception, e:
        print e
        self.oldTime = time.time()
        self.oldPos  = self.getPos()
    updateFromBody( self, self.body )
    p = self.getRelativePoint( self.bodyNode, panda.VBase3( 0, 0, 0 ) )
    p = render.getRelativePoint( self, -p )
    panda.NodePath.setPos( self, p )
    
    for w in self.wheels:
      updatePosFromBody( w["node"], w["body"] )
      p = self.getRelativePoint( render, w["node"].getPos() )
