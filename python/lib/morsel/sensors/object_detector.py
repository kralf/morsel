from morsel.core.framework import *

class ObjectDetector:
  def __init__( self, name ):
    self.objects = []
    self.sensors = []
    self.detections = []
    self.name = name
    self.bounds = {}
    scheduler.addTask( name + "DetectorTask", self.update )
    
#-------------------------------------------------------------------------------

  def getBounds( self, obj ):
    if not self.bounds.has_key( obj ):
      b = obj.getTightBounds()
      self.bounds[obj] = [
        obj.getRelativePoint( render, b[0] ), 
        obj.getRelativePoint( render, b[1] )
      ]
    return self.bounds[obj]
    
#-------------------------------------------------------------------------------

  def addSensor( self, sensor ):
    self.sensors.append( sensor )
  
#-------------------------------------------------------------------------------
  
  def addObject( self, obj, obj_type ):
    self.objects.append( [obj, obj_type] )
    
#-------------------------------------------------------------------------------

  def update( self, time ):
      del self.detections[:]
      # We'll obtain consecutive ID's as signatures (HACK!)
      i = 0
      for o in self.objects:
        for s in self.sensors:
          if s.inRange( o[0] ):
            self.detections.append( [s, o[0], o[1], i] )
        i += 1
      return True
