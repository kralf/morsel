from morsel.core   import *
from pickle import *

#-------------------------------------------------------------------------------

class Player:
  def __init__( self, node = None, filename = None ):
    self.filename = filename
    self.playing = False
    self.setup( node, findFile( filename ) )
    scheduler.addTask( filename, self.step, 0 )
    
  def playing( self ):
    return self._playing
    
  def setup( self, node, filename ):
    if node and filename:
      self.node = node
      self.filename = filename
      self.track = load( open( filename ) )
      self.playing = False
      self.frame = 0
    else:
      print "Error: node or filename not specified"
      exit( 1 )
  
  def start( self ):
    self.setup( self.node, findFile( self.filename ) )
    self.playing = True
    self.frame = 0
    
  def stop( self ):
    self.playing = False
    
  def step( self, time ):
    if ( self.playing ):
      position = self.track[self.frame][0]
      heading  = self.track[self.frame][1]
      delay    = self.track[self.frame][2]
      self.node.setPos( *position )
      self.node.setHpr( *heading )
      self.frame = ( self.frame + 1 ) % len( self.track )
      return delay
    return True
