from morsel.core import *
import _platforms

#-------------------------------------------------------------------------------

meshes = {}

#-------------------------------------------------------------------------------

def Mesh( name, filename, position = [0, 0, 0], orientation = [0, 0, 0], scale = 1, selectable = True, terrain = False, body = True ):
  '''Loads an .egg or .bam mesh an puts it in the world.'''  
  if name in meshes:
    return meshes[name]
  mesh = loadMesh( name, filename )
  mesh.setName( name )
  mesh.setPos( *position )
  mesh.setHpr( *orientation )
  mesh.reparentTo( render )
  meshes[name] = mesh
  if body:
    _platforms.registerBody( name, mesh, terrain )
  return mesh
  

#-------------------------------------------------------------------------------

def Actor( name, filename, position = [0, 0, 0], animation = None, orientation = [0, 0, 0], scale = 1, selectable = True ):
  '''Loads an .egg or .bam actor an puts it in the world.'''

  actor = loadActor( name, filename, animation, selectable )
  actor.setPos( *position )
  actor.setHpr( *orientation )
  actor.setScale( scale )
  return actor

#-------------------------------------------------------------------------------

def attachCamera( object, position = [ -5, 2, 5], lookAt = [5, 0, 0], camera = base.camera ):
  '''Attaches a camera to the given object'''
  camera.reparentTo( object )
  camera.setPos( *position )
  camera.lookAt( *lookAt )
  mat = panda.Mat4( camera.getMat() )
  mat.invertInPlace()
  base.mouseInterfaceNode.setMat( mat )

#-------------------------------------------------------------------------------

def showFPS( value ):
    '''Shows the Frames Per Second in the upper right part of the screen.'''
    base.setFrameRateMeter( value )

#-------------------------------------------------------------------------------

def PointLight( name, position, color = panda.Vec4( 1, 1, 1, 1 ), attenuation = False ):
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
    frame = loader.loadModel( "zup-axis.egg" )
    frame.reparentTo( object )
    frame.setScale( scale )
    frame.setPos( 0, 0, 0 )
    frame.setHpr( 0, 0, 0 )
    frame.node().adjustDrawMask( panda.PandaNode.getAllCameraMask(), panda.BitMask32( '001' ), panda.BitMask32( '0' ) )
    return frame

