from globals import *
from shared  import *
from morsel.platforms.functions import *
from morsel.core import *

#-------------------------------------------------------------------------------

class World:
  def __init__( self ):
    self.platforms = []
    self.bodies    = []
    self.period    = 0.01
    self.delta     = 0
    self.lastTime  = 0
    self.setupOde()
    scheduler.addTask( "WorldUpdater", self.update )
  
  #-----
  
  def setupOde( self ):
    self.world   = panda.OdeWorld()
    self.world.setGravity( 0, 0, -9.81 )
    self.world.initSurfaceTable( 1 )
    self.world.setContactSurfaceLayer( 0.01 )
    self.world.setSurfaceEntry( 
      0, 0, mu = 100, 
      bounce = 0.3, bounce_vel = 10, 
      soft_erp = 0.8, soft_cfm = 1E-10, 
      slip = 0.1, dampen = 0 )
    self.space   = panda.OdeSimpleSpace()
    self.space.setAutoCollideWorld( self.world )
    self.space.enable()
    self.collisionGroup = panda.OdeJointGroup()
    self.space.setAutoCollideJointGroup( self.collisionGroup )

  #-----
  
  def registerBody( self, name, mesh, terrain ):
    mesh.setCollideMask( panda.BitMask32.bit( 0 ) )
    pos      = mesh.getPos()
    geometry = None
    if terrain:
      #print "Descendants", mesh.countNumDescendants()
      #print "Bounds", mesh.getTightBounds()
      #mesh.flattenStrong()
      #mesh.writeBamFile( "g.bam" )
      #mesh.setTwoSided( True )
      data     = panda.OdeTriMeshData( mesh.getChild( 0 ) )
      geometry = panda.OdeTriMeshGeom( self.space, data )
      #exit()
    else:
      geometry = panda.OdeBoxGeom( self.space, *bounds( mesh ) )
    geometry.setPosition( pos[0], pos[1], pos[2] )
    geometry.setQuaternion( mesh.getQuat() )
    geometry.setCategoryBits( STATIC_CATEGORY )
    geometry.setCollideBits( STATIC_COLLIDE_BITS )
    self.bodies.append( { "geometry": geometry, "mesh": mesh } )
  
  #-----
  
  def addPlatform( self, name, platform_type, position, orientation ):
    platform =  loadPlatform( "ode", platform_type, [name, self], position, orientation )
    self.platforms.append( platform )
    return platform
    
  #-----
  
  def update( self, time ):
    self.delta += time - self.lastTime
    update = self.delta > self.period
    while self.delta > self.period:
      contactPoints = self.space.autoCollide()
      for p in self.platforms:
        p.updatePhysics( self.period )
      self.world.quickStep( self.period )
      self.collisionGroup.empty()
      self.delta -= self.period
    if update:
      for p in self.platforms:
        p.updateGraphics()
    self.lastTime = time
    return True