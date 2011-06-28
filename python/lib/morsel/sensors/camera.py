from morsel.core import *

#-------------------------------------------------------------------------------

class Camera( panda.NodePath ):
  def __init__( self, name, width, height, hFov = 90, vFov = 90, near = 0.1, far = 100, depth = False ):
    panda.NodePath.__init__( self, name )
    self.width   = width
    self.height  = height
    self.vFov   = vFov
    self.hFov   = hFov
    self.near    = near
    self.far     = far
    self.visible = False
    self.depth   = depth

    self.texture = panda.Texture() 
    self.buffer = base.win.makeTextureBuffer( 'texture', width, height, self.texture, True )
    
    if depth:
      self.depth_texels  = panda.PNMImage()
      self.depth_texture = panda.Texture() 
      self.depth_texture.setFormat( panda.Texture.FDepthComponent )
      self.depth_texture.setComponentType( panda.Texture.TUnsignedShort )
      self.depth_buffer = base.win.makeTextureBuffer( 'depth_texture', width, height, self.depth_texture, True )

    
    self.camNode = panda.Camera( name )
    self.camNode.setCameraMask( panda.BitMask32( '001' ) )
    self.lens = self.camNode.getLens()
    self.lens.setNearFar( self.near, self.far )
    self.lens.setFov( self.hFov )
    self.lens.setAspectRatio( 1.0 * self.hFov / self.vFov )
    
    self.camera = self.attachNewNode( self.camNode )
    self.camera.setName( "camera" )

    self.display_region = self.buffer.makeDisplayRegion()
    self.display_region.setSort( -10 );
    self.display_region.setCamera( self.camera )      

    if depth:
      self.depth_display_region = self.depth_buffer.makeDisplayRegion()
      self.depth_display_region.setSort( -20 );
      self.depth_display_region.setCamera( self.camera )  
      
  def save( self, filename, depthFilename = None ):
    texels  = panda.PNMImage()
    self.texture.store( texels )
    texels.write( panda.Filename( filename ) )
    if depthFilename and self.depth:
      near = self.camNode.getLens().getNear()
      far  = self.camNode.getLens().getFar()
      texels  = panda.PNMImage()
      self.depth_texture.store( texels )
      for x in xrange( self.width ):
        for y in xrange( self.height ):
          depth = texels.getGray( x, y )
          value = far * near / ( far - depth * ( far - near ) )
          texels.setGray( x, y, value / far )
      texels.write( panda.Filename( depthFilename ) )

  def setScene( self, node ):
    self.camera.node().setScene( node )
    
  def show(self, left = 0, right = 1, bottom = 0, top = 1 ):
    if not self.visible:
      self.visible = True
      cm = panda.CardMaker( self.getName() )
      cm.setFrame( left, right, bottom, top )
      self.cardNode = cm.generate()
      self.card = render2d.attachNewNode( self.cardNode )
      self.card.setTexture( self.texture )
    
  def hide( self ):
    if self.visible:
      self.visible = False
      self.card.removeNode()
