from morsel.core.framework import *
from morsel.platforms.car import *

class FileStateOut( object ):
  
  def __init__( self, filename, car ):
    self.filename  = filename
    if type( car ) == Car:
      self.car  = car.node
    else:
      self.car  = car
    self.file      = open( self.filename, "w" )
    scheduler.addTask( "fileStateOut", self.step )
        
  def step( self, time ):
    position    = self.car.getPos()
    orientation = self.car.getHpr()
    self.file.write( "%.2f %.2f %.2f\n" % ( position[0], position[1], position[2] ) )
    self.file.flush()
    return True
