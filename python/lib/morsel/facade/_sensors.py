from morsel.core import *
from morsel.morselc import RangeSensor as CRangeSensor
import morsel.sensors

#-------------------------------------------------------------------------------

def LaserScanner(  name, parent, position = [0, 0, 0], orientation = [0, 0, 0],
                      hFov = 180, vFov = 0.1, hRayCount = 360, vRayCount = 1,
                      rayRange = [1, 10], period = None, createTask = True, cameraFOV = 60,
                      colorInfo = False ):
  '''Adds a single plane laser scanner to the parent object.'''
  result = CRangeSensor( name, hFov, vFov, hRayCount, vRayCount,
    rayRange[0], rayRange[1], cameraFOV, colorInfo )
  if createTask:
    scheduler.addTask( name + "Task", result.update, period, priority = 5  )
  result.reparentTo( parent )
  result.setPos( *position )
  result.setHpr( *orientation )
  return result

#-------------------------------------------------------------------------------

def Odometry(  name, parent, period = None):
  '''Adds an odometry sensor to the parent object.'''
  result = OdometrySensor( name, parent, period )
  result.reparentTo( parent )
  return result

#-------------------------------------------------------------------------------

def _Camera( 
    name, parent, 
    width = 512, height = 512, 
    hFov = 90, vFov = 90, near = 0.1, far = 100, depth = False, 
    position = [0, 0, 0], orientation = [0, 0, 0] ):
  result = sensors.Camera( 
    name, width, height, 
    hFov, vFov, near, far, depth )
  result.setScene( render )
  result.reparentTo( parent )
  result.setPos( *position )
  result.setHpr( *orientation )
  return result
