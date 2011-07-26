from morsel.core import *
import morsel.world

#-------------------------------------------------------------------------------

def Mesh_( name, filename, position = [0, 0, 0], orientation = [0, 0, 0],
          scale = 1, two_sided = False ):
  if world != None:
    mesh = world.addMesh( name, filename )
    mesh.setPos( *position )
    mesh.setHpr( *orientation )
    mesh.setScale( scale )
    mesh.setTwoSided( two_sided )
      
    return mesh
  else:
    raise RuntimeError( "World not initialized" )  

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

#-------------------------------------------------------------------------------

def attachCamera( object, position = [ -5, 2, 5], lookAt = [0, 0, 0],
                  camera = base.camera, rotate = False ):
  '''Attaches a camera to the given object'''
  camera.reparentTo( object )
  camera.setPos( *position )
  camera.lookAt( *lookAt )
  mat = panda.Mat4( camera.getMat() )
  mat.invertInPlace()
  base.mouseInterfaceNode.setMat( mat )
  if rotate == False:
    camera.setEffect( panda.CompassEffect.make(render) )

#-------------------------------------------------------------------------------

def showFPS( value ):
    '''Shows the Frames Per Second in the upper right part of the screen.'''
    base.setFrameRateMeter( value )
