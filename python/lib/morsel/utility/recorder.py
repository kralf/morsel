from morsel.panda import *
from pickle import *

#-------------------------------------------------------------------------------

class Recorder:
  def __init__( self, node, filename, period = None ):
    self.node = node
    self.filename = filename
    self.track = []
    self.recording = False
    self.lastTime = -1;
    scheduler.addTask( self.node.getName() + "Recorder", self.step, period )
    
  def recording( self ):
    return self.recording
  
  def start( self ):
    self.recording = True
    self.frame = 0
    self.lastTime = -1
    
  def stop( self ):
    self.recording = False
    
  def save( self ):
    f = open( self.filename, "w" )
    dump( self.track, f )
    f.close()
  
  def step( self, time ):
    if ( self.recording ):
      if self.lastTime == -1:
        delay = 0
      else:
        delay = time - self.lastTime
      if delay == 0:
        delay  = 0.00001
      self.lastTime = time
        
      position = self.node.getPos()
      heading  = self.node.getHpr()
      self.track.append( [[position[0], position[1], position[2]], [heading[0], heading[1], heading[2]], delay] )
    return True
