from morsel.core.framework import *

from panda3d.pandac.Modules import Point3
from panda3d.pandac.Modules import PNMImage
from panda3d.pandac.Modules import Texture
from panda3d.pandac.Modules import Vec4
from panda3d.pandac.Modules import VBase3

from panda3d.pandac.Modules import BitMask32
from panda3d.pandac.Modules import PandaNode
from panda3d.pandac.Modules import NodePath

from math import *

class LaserScanner( NodePath ):
  def __init__( self, name, fov = 180, rayCount = 360, rayRange = [1, 10], period = 0.04 ):
    NodePath.__init__( self, name )
    self.width    = 512
    self.height   = 1
    self.fov = fov
    self.rayCount = rayCount
    self.rayRange = rayRange
    self.period = period
    self.setupCameras()
    self.last = None
    scheduler.addTask( name + "Task", self.step, period  )

#-------------------------------------------------------------------------------

  def step( self, time ):
    for i in range( 0, self.cameraCount ):
      self.depthmaps[i].store( self.texels[i] )
    self.updateRays()
    return True

#-------------------------------------------------------------------------------

  def setupCameras( self ):
    self.cameraCount = int( ceil( self.fov / 90.0 ) )
    startAngle = self.fov / 2
    cameraFov  = self.fov / self.cameraCount
    self.texels       = []
    self.depthmaps    = []
    self.depthbuffers = []
    self.cameras      = []
    self.rays         = [[]] * self.rayCount
    self.precomp      = []
    self.deltaAngle   = -(pi / 180) * self.fov / (self.rayCount - 1 )
    residual = 0
    for i in range( 0, self.cameraCount ):
      self.setupRenderBuffer( i, startAngle - i * cameraFov, cameraFov )
      residual = self.setupRays( i, startAngle - i * cameraFov, residual, cameraFov )

#-------------------------------------------------------------------------------

  def setupRenderBuffer( self, number, startAngle, cameraFov ):
    self.texels.append( PNMImage() )
    self.depthmaps.append( Texture() )
    self.depthmaps[number].setFormat( Texture.FDepthComponent )
    self.depthmaps[number].setComponentType( Texture.TUnsignedShort )
    self.depthbuffers.append( base.win.makeTextureBuffer( 'depthmap', self.width, self.height, self.depthmaps[number], True ) )
    self.cameras.append( base.makeCamera( self.depthbuffers[number] ) )
    self.cameras[number].reparentTo( self )
    
    self.cameras[number].node().setScene( render )
    self.cameras[number].node().getLens().setNearFar( *self.rayRange )
    self.cameras[number].setHpr( -90 + startAngle - cameraFov / 2 , 0, 180 )
    self.cameras[number].node().getLens().setFov( cameraFov )
    self.cameras[number].node().setCameraMask( BitMask32( '001' ) )
    self.cameras[number].setLightOff( 1 )
    self.cameras[number].setMaterialOff( 1 )
    self.cameras[number].setColorOff( 1 )

#-------------------------------------------------------------------------------

  def setupRays( self, number, startAngle, residual, cameraFov ):
    fov        = cameraFov * pi / 180
    angle      = fov / 2 + residual
    focal = ( self.width / 2 - 0.5) / tan( fov / 2 )
    while angle + fov / 2 > -2e-10:
      height    = focal * tan( angle )
      cell      = int( self.width / 2 + height )
      self.precomp.append( [angle, number, cell, tan( angle ), startAngle * pi / 180 + angle - fov / 2] )
      angle += self.deltaAngle
    return fov / 2 + angle

#-------------------------------------------------------------------------------
    
  def updateRays( self ):
    i = 0
    for rayInfo in self.precomp:
      texture = rayInfo[1]
      cell    = rayInfo[2]
      depth   = self.texels[texture].getGray( cell, 0 )
      x = self.rayRange[1] * self.rayRange[0] / ( self.rayRange[1] - depth * ( self.rayRange[1] - self.rayRange[0] ) )
      if x < 0:
        x = 0
      y = x * rayInfo[3]
      r = sqrt( x * x + y * y )
      x = r * cos( rayInfo[4] )
      y = r * sin( rayInfo[4] )
      if r >= self.rayRange[1]:
        r = -1
      self.rays[i] = [x, y, 0, r]
      i += 1

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
