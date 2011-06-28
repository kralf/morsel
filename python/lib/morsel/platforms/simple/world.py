from morsel.core import *
import platforms.functions as functions

#-------------------------------------------------------------------------------

class World:
  def __init__( self ):
    self.platforms = []
    self.period    = 0.01
    self.delta     = 0
    self.lastTime  = 0
    scheduler.addTask( "WorldUpdater", self.update )
    
  #-----
  
  def registerBody( self, name, mesh, terrain ):
    mesh.setCollideMask( panda.BitMask32.bit( 0 ) )

  #-----
  
  def addPlatform( self, name, platform_type, position, orientation ):
    platform =  functions.loadPlatform( "simple", platform_type, [name], position, orientation )
    self.platforms.append( platform )
    return platform

  #-----
  
  def update( self, time ):
    self.delta += time - self.lastTime
    update = self.delta > self.period
    while self.delta > self.period:
      for p in self.platforms:
        p.updatePhysics( self.period )
      self.delta -= self.period
    if update:
      for p in self.platforms:
        p.updateGraphics()
    self.lastTime = time
    return True