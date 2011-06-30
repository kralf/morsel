import morsel.viewers
from morsel.morselc import LaserViewer as CLaserViewer
from morsel.core import *

#-------------------------------------------------------------------------------

def LaserViewer( laser, color = [1, 0, 0, 0], period = None, points = False, colorInfo = False ):
  '''Allows visualisation of a laser scanner'''
  result = CLaserViewer( laser.getName() + "Viewer", laser,
    color[0], color[1], color[2], color[3], points, colorInfo )
  result.reparentTo( laser )
  scheduler.addTask( laser.getName() + "ViewerTask", result.update, period, priority = 10 )
  return result
