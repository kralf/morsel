from globals import *
from shared  import *
from morsel.core    import *
from math    import *
import time

DEBUG = False

#-------------------------------------------------------------------------------

class Differential( panda.NodePath ):
  def __init__( self, name, world, mesh = None, pivot = None,
                      propulsionForce = None,
                      vehicleMass = None, massOffset = None,
                      wheelMass = None, wheelRadius = None, wheelDistance = None,
                      maxSpeed = None, maxRotationalVelocity = None,
                      **kargs ):
    NodePath.__init__( self, name )
    self.mesh  = loadMesh( name + "Mesh", mesh )
    self.mesh.reparentTo( self )
    self.mesh.setPos( - panda.VBase3( *pivot ) )
    
    self.command               = [0, 0]
    self.propulsionForce       = propulsionForce
    self.vehicleMass           = vehicleMass
    self.massOffset            = massOffset
    self.wheelMass             = wheelMass
    self.wheelRadius           = wheelRadius
    self.wheelDistance         = wheelDistance
    self.maxSpeed              = maxSpeed
    self.maxRotationalVelocity = maxRotationalVelocity
    
    self.world        = world.world
    self.odeTimeDelta = world.period
    self.space        = world.space
    
    
    self.setCommand( [0, 0] )
    self.commandSize = 2
    self.commandLimits = [
      ( -maxSpeed, maxSpeed),
      ( -maxRotationalVelocity, maxRotationalVelocity )
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
    if self.wheelDistance == None:
      self.wheelDistance    = self.lengthY - 2 * self.wheelRadius
    
  #-----
  
  def setupChassis( self ):
    self.body = panda.OdeBody( self.world )
    self.body.setPosition( *self.massOffset )
    self.body.setQuaternion( panda.Quat( 1, 0, 0, 0 ) )

    self.mass = panda.OdeMass()
    self.mass.setBoxTotal( 
      self.vehicleMass, 
      self.wheelDistance, 
      self.wheelDistance, 
      2 * self.wheelRadius )
      
    self.bodyNode = panda.NodePath( "massNode" )
    self.bodyNode.reparentTo( self )
    self.bodyNode.setPos( 0, 0, 0 )

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
      centerNode.setPos( 0, 0, 0 )
      
      mesh = loadMesh( self.getName() + "_mass", "geometry/cube.bam" )
      mesh.setScale( 
        self.wheelDistance, 
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
    
    for i in xrange( 2 ):
      if i % 2 == 0:
        y =  self.wheelDistance / 2
      else:
        y = -self.wheelDistance / 2

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
      joint.setParamFMax( 0, 1000 )
      joint.setParamFMax( 1, self.propulsionForce )
      joint.setParamSuspensionERP( 0, erp( self.vehicleMass, 0.5, 0.05, self.odeTimeDelta ) )
      joint.setParamSuspensionCFM( 0, cfm( self.vehicleMass, 0.5, 0.05, self.odeTimeDelta ) ) 

      joint.setParamLoStop( 0, 0 )
      joint.setParamHiStop( 0, 0 )
        
      self.wheels.append( { "body": body, "geometry": geometry, "joint": joint, "node": wnode } )

    x = 0
    y = 0
    z = -self.wheelRadius / 2
    
    for i in xrange( 2 ):
      if i % 2 == 0:
        x =  self.wheelDistance / 2
      else:
        x = -self.wheelDistance / 2
        
      wgeom = panda.GeomNode( "w%i" % ( i + 2 ) )
      wnode = render.attachNewNode( wgeom )
      wgeom.setBounds( panda.BoundingSphere( panda.Point3(0, 0, 0), self.wheelRadius / 2 ) )
      wgeom.setFinal( 1 )
      wnode.setPos( x, y, z)
      
      if DEBUG:
        wnode.showBounds()
        
      
      mass = panda.OdeMass()
      mass.setSphereTotal( self.wheelMass, self.wheelRadius / 2 )
      
      body = panda.OdeBody( self.world )
      body.setMass( mass )
      body.setPosition( x, y, z )
      body.setQuaternion( panda.Quat( 1, 0, 0, 0 ) )

      geometry = panda.OdeSphereGeom( self.space, self.wheelRadius / 2 )
      geometry.setBody( body )
      geometry.setCategoryBits( ACTUATOR_CATEGORY )
      geometry.setCollideBits( ACTUATOR_COLLIDE_BITS )
      
      joint = panda.OdeBallJoint( self.world )
      joint.attach( self.body, body )
      joint.setAnchor( x, y, z )
      self.wheels.append( { "body": body, "geometry": geometry, "joint": joint, "node": wnode } )
      
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
    return self.velocity, self.rotationalVelocity

  def setCommand( self, command ):
    self.velocity, self.rotationalVelocity = command

  command = property( getCommand, setCommand )
  
  #-----
  
  def updatePhysics( self, period ):
    vLeft  = ( self.velocity - 0.5 * self.wheelDistance * self.rotationalVelocity ) \
             / self.wheelRadius
    vRight = ( self.velocity + 0.5 * self.wheelDistance * self.rotationalVelocity ) \
             / self.wheelRadius
    if DEBUG:
      print "V:%f W:%f VL:%f VR:%f" % ( self.velocity, self.rotationalVelocity, vLeft, vRight )
    self.wheels[0]["joint"].setParamVel( 1, vLeft )
    self.wheels[1]["joint"].setParamVel( 1, vRight )
      
  #-----
  
  def updateGraphics( self ):
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
        print "Velocity:", distance / delta, delta
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
      updateHprFromBody( w["node"], w["body"] )
      p = self.getRelativePoint( render, w["node"].getPos() )
