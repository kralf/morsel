from morsel.panda import *
import morsel.world

#-------------------------------------------------------------------------------

def PointLight( name, position, color = panda.Vec4( 1, 1, 1, 1 ),
                attenuation = False ):
  light = panda.PointLight( name )
  light.setColor( color )
  if attenuation:
    light.setAttenuation( attenuation )
  lightNode = render.attachNewNode( light )
  lightNode.setPos( position[0], position[1], position[2] )
  render.setLight( lightNode )
  return light, lightNode

#-------------------------------------------------------------------------------

def AmbientLight( name, color = panda.VBase4( 0.5, 0.5, 0.5, 1 ) ):
  light = panda.AmbientLight( name )
  light.setColor( color )
  lightNode = render.attachNewNode( light )
  render.setLight( lightNode )
  return light, lightNode

#-------------------------------------------------------------------------------

def Frame( object, scale = 0.5 ):
    frame = loader.loadModel( "zup_axis.egg" )
    frame.reparentTo( object )
    frame.setScale( scale )
    frame.setPos( 0, 0, 0 )
    frame.setHpr( 0, 0, 0 )
    frame.node().adjustDrawMask( panda.PandaNode.getAllCameraMask(),
      panda.BitMask32( '001' ), panda.BitMask32( '0' ) )
    return frame
