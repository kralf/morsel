from sensors.range_camera import RangeCamera as PythonRangeCamera
from morsel.core.framework import *

from panda3d.pandac import BitMask32
from panda3d.pandac import NodePath
from panda3d.pandac import VBase3

from math import *

class RangeSensor( NodePath ):
  def __init__( 
    self, 
    name, 
    hFov = 90, 
    vFov = 90, 
    hRayCount = 360, 
    vRayCount = 360, 
    rayRange = [1, 10], 
    period = None
  ) :
    NodePath.__init__( self, name )
    self.hFov = 1.0 * hFov
    self.vFov = 1.0 * vFov
    self.hRayCount = hRayCount
    self.vRayCount = vRayCount
    self.rayCount  = hRayCount * vRayCount
    self.rayRange  = rayRange
    self.cameras   = []
    self.rays      = [[]] * self.rayCount
    self.setupCameras()
    scheduler.addTask( name + "Task", self.update, period  )

#-------------------------------------------------------------------------------

  def update( self, time ):
    i = 0
    ci = 0
    base.graphicsEngine.renderFrame()
    for c in self.cameras:
      c.update( time )
      for ri in range( c.rayCount ):
        ray = c.rays[ri]
        p = self.getRelativePoint( c, VBase3( ray[2], ray[3], ray[4] ) )
        r = sqrt( p[0] * p[0] + p[1] * p[1] + p[2] * p[2] )
        if r >= self.rayRange[1]:
          r = -1
        self.rays[i] = [
          self.startHRays[ci] + ray[0], 
          self.startVRays[ci] + ray[1], 
          p[0], p[1], p[2], r
        ] 
        i += 1
      ci += 1
    return True
      

#-------------------------------------------------------------------------------
    
  def computeParameters( self, fov, rayCount ):
    fovs      = []
    angles    = []
    rayCounts = []
    covered   = 0
    if rayCount > 1:
      inc = fov / ( rayCount - 1 )
    else:
      inc = fov
    angle = - fov / 2
    while covered <= fov:
      toCover = fov - covered
      if toCover > 60:
        toCover = 60
      if rayCount != 1:
        rays = floor( toCover / inc )
        rayCounts.append( int(rays) + 1 )
      else:
        rays = 1
        rayCounts.append( 1 )
      toCover = rays * inc
      angles.append( angle + toCover / 2 )
      fovs.append( toCover )
      angle += toCover + inc
      covered += toCover + inc
    
    if sum( rayCounts ) < rayCount:
      rayCounts[-1] += 1
    return ( fovs, angles, rayCounts )
    
    
#------------------ -------------------------------------------------------------

  def setupCameras( self ):
    hFovs, hAngles, hRayCount = self.computeParameters( self.hFov, self.hRayCount )
    vFovs, vAngles, vRayCount = self.computeParameters( self.vFov, self.vRayCount )
    self.startHRays = []
    self.startVRays = []
    hRays = 0
    for i in range( len( hFovs ) ):
      vRays = 0
      for j in range( len( vFovs ) ):
        #print "fovs:", hFovs[i], vFovs[j]
        c = PythonRangeCamera( 
          "%s:%i,%i" % (self.getName(), i, j ),
          hFovs[i], 
          vFovs[j], 
          hRayCount[i], 
          vRayCount[j],
          self.rayRange
        )
        c.reparentTo( self )
        c.setHpr( hAngles[i], vAngles[j], 0 )
        #c.camera.node().showFrustum()
        self.cameras.append( c )
        self.startHRays.append( hRays )
        self.startVRays.append( vRays )
        vRays += vRayCount[j]
      hRays += hRayCount[i]
      
#-------------------------------------------------------------------------------

  def inRange( self, node ):
    ''' Returns true if node is in the sensor's range.
    TODO: Take into account FOV.
    '''
    p = self.getRelativePoint( node, VBase3( 0, 0, 0 ) )
    distance = sqrt( p.dot( p ) )
    if distance >= self.rayRange[0] and distance <= self.rayRange[1]:
      if p[0] > 0:
        return True
    return False