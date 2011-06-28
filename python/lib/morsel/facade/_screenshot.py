from morsel.core import *

#-------------------------------------------------------------------------------

frame_number = 0
video_status = False

#-------------------------------------------------------------------------------

def pad( number ):
  return str( number ).rjust( 4, "0" )  

#-------------------------------------------------------------------------------

def timeToString( time ):
  left, right = str( time ).split( '.' )
  return left.rjust( 4, "0" )[:4] + "_" + right.ljust( 4, "0" )[:4]
  
#-------------------------------------------------------------------------------

def saveScreenshot( time ):
  global frame_number
  frame_str = pad( frame_number )
  time_str  = timeToString( time )
  base.win.saveScreenshot( panda.Filename( 'f%s_%s.jpg' % ( frame_str, time_str ) ) )
  frame_number += 1

#-------------------------------------------------------------------------------

def make_video():
  global video_status
  global frame_number
  if video_status:
     scheduler.removeTask("Video")
     video_status = False
  else:
     video_status = True
     frame_number = 0
     scheduler.addTask("Video", recordFrames, period = 1.0 / 24 )

#-------------------------------------------------------------------------------

def recordFrames(time):
   global frame_nb
   saveScreenshot( time )
   return True

