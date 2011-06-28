from panda3d.pandac.Modules import Point3
from panda3d.pandac.Modules import PNMImage
from panda3d.pandac.Modules import Texture
from panda3d.pandac.Modules import Vec4
from panda3d.pandac.Modules import VBase3

from panda3d.pandac.Modules import BitMask32
from panda3d.pandac.Modules import PandaNode
from panda3d.pandac.Modules import NodePath

from math import *

class RangeCamera( NodePath ):
  def __init__( 
    self, 
    name, 
    hFov = 90, 
    vFov = 90, 
    hRayCount = 360, 
    vRayCount = 360, 
    rayRange = [1, 10]
  ) :
    NodePath.__init__( self, name )
    self.width  = 128
    self.height = 128
    self.hFov = hFov
    self.vFov = vFov
    self.hRayCount = hRayCount
    self.vRayCount = vRayCount
    self.rayRange = rayRange
    self.precomp  = []
    self.rays     = [[]] * (self.hRayCount * self.vRayCount)
    self.rayCount = self.hRayCount * self.vRayCount
    self.setupCamera()
    self.setupRays()
    
#-------------------------------------------------------------------------------

  def update( self, time ):
    #print self.depthmap.get_size_x()
    self.depthmap.store( self.texels )
    self.updateRays()
    return True

#-------------------------------------------------------------------------------

  def setupCamera( self ):
    hStartAngle      = self.hFov / 2.0
    vStartAngle      = self.vFov / 2.0
    self.texels      = PNMImage()
    self.depthmap    = Texture() 
    
    self.depthmap.setFormat( Texture.FDepthComponent )
    self.depthmap.setComponentType( Texture.TUnsignedShort )
    
    self.depthbuffer = base.win.makeTextureBuffer( 'depthmap', self.width, self.height, self.depthmap, True )
    self.camera      = base.makeCamera( self.depthbuffer )
    
    self.camera.reparentTo( self )
    
    self.camera.node().setScene( render )
    self.camera.node().getLens().setNearFar( *self.rayRange )
    self.camera.setHpr( -90, 0, 180 )
    self.camera.node().getLens().setFov( self.hFov )
    self.camera.node().getLens().setAspectRatio( 1.0 * self.hFov / self.vFov )
    self.camera.node().setCameraMask( BitMask32( '001' ) )
    self.camera.setLightOff( 1 )
    self.camera.setMaterialOff( 1 )
    self.camera.setColorOff( 1 )

#-------------------------------------------------------------------------------

  def setupRays( self ):
    hFov        = self.hFov * pi / 180
    vFov        = self.vFov * pi / 180
    if self.hRayCount > 1:
      deltaHAngle = -hFov / (self.hRayCount - 1 )
      hAngle      = hFov / 2
    else:
      deltaHAngle = -hFov
      hAngle      = 0
    if self.vRayCount > 1:
      deltaVAngle = -vFov / (self.vRayCount - 1 )
    else:
      deltaVAngle = -vFov
    hFocal = ( self.width / 2 - 0.5) / tan( hFov / 2 )
    vFocal = ( self.height / 2 - 0.5) / tan( vFov / 2 )
    while hAngle + hFov / 2 > -2e-10:
      hDist = hFocal * tan( hAngle )
      col   = int( self.width / 2 + hDist )
      if self.vRayCount > 1:
        vAngle      = vFov / 2
      else:
        vAngle      = 0
      while vAngle + vFov / 2 > -2e-10:
        vDist = vFocal * tan( vAngle )
        row   = int( self.height / 2 + vDist )
        self.precomp.append( [
          hAngle, vAngle, 
          col, row, 
          tan( hAngle ), tan( vAngle ), 
          hAngle,
          vAngle,
        ] )
        vAngle += deltaVAngle
      hAngle += deltaHAngle
      
#-------------------------------------------------------------------------------
    
  def updateRays( self ):
    i = 0
    for rayInfo in self.precomp:
      col    = rayInfo[2]
      row    = rayInfo[3]
      depth   = self.texels.getGray( col, row )
      x = self.rayRange[1] * self.rayRange[0] / ( self.rayRange[1] - depth * ( self.rayRange[1] - self.rayRange[0] ) )
      if x < 0:
        x = 0
      y = x * rayInfo[4]
      z = x * rayInfo[5]
      r = sqrt( x*x + y*y + z*z )
      self.rays[i] = [col, row, x, y, z]
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
