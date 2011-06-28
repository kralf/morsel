from morsel.core.framework import *
from panda3d.pandac.Modules import VBase3
from math import *

class FileAXTOut( object ):
  def __init__( self, filename, laserScanner ):
    self.filename = filename
    self.file = open( filename, "w" )
    self.laserScanner = laserScanner
    scheduler.addTask( "fileAXTOut", self.step )

#-------------------------------------------------------------------------------

  def step( self, time ):
    #TODO: This is not working, check why
    #self.axtScan.header.timestamp = smart_comm.getTime()
    if len( self.laserScanner.rays[0] ) == 6:
      for i in range( 0, self.laserScanner.rayCount ):
        ray = self.laserScanner.rays[i]
        if ray[5] >= 0:
          p = render.getRelativePoint( self.laserScanner, VBase3( *ray[2:5] ) )
          self.file.write( "%.2f %.2f %.2f\n" % ( p[0], p[1], p[2] ) )
          self.file.flush()
    return True
