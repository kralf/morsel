''' @package Framework.
This package contains framework specific functions that are primarily intended
to be used by programmers.
'''

import panda3d.pandac as panda
from panda3d.direct.actor import Actor as pandaActor
from morsel.config import *
import math
import os.path
import os
import inspect

#-------------------------------------------------------------------------------
# Logging functions
#-------------------------------------------------------------------------------

def error( message ):
  print "Usage: morsel configfile"
  print
  print "ERROR:", message
  exit()

#-------------------------------------------------------------------------------
# Object list functions
#-------------------------------------------------------------------------------

def loadMesh( name, filename, selectable = True, twoSided = True ):
  '''Loads an .egg or .bam mesh and adds it to the object list.'''
  meshfile = findFile( filename )
  if meshfile:
    mesh = loader.loadModel( meshfile )
    if selectable:
      meshes[name] = mesh
    mesh.setTwoSided( twoSided )
    return mesh
  else:
    exit( 1 )


def loadActor( name, filename, animation = None, selectable = True ):
  '''Loads an .egg or .bam actor and adds it to the actor list.'''
  actorfile = findFile( filename )
  if not animation:
    animation = os.path.splitext( os.path.basename( filename ) )[0]
  if actorfile:
    actor = pandaActor.Actor( actorfile )
    actor.reparentTo( render )
    actor.node().setBounds( panda.OmniBoundingVolume() )
    actor.node().setFinal( True )
    actors[name] = [  actor,
                      animation,
                      actor.getDuration( animation ),
                      actor.getNumFrames( animation )]
    return actor
  else:
    exit( 1 )

def updateActors( time ):
  '''Actor update task'''
  for actor, animation, duration, frames in actors.values():
    frameTime = time - math.floor( time / duration ) * duration
    if frameTime == 0:
      frame = 0
    else:
      frame     = int( frames * frameTime / duration )
    actor.pose( animation, frame )
    actor.forceRecomputeBounds()
  return True


#-------------------------------------------------------------------------------
# File utility functions
#-------------------------------------------------------------------------------

def includeConfig( filename ):
  configFile = findFile( filename )
  if configFile:
    context = inspect.stack()[1][0].f_globals
    execfile( configFile, context )
  else:
    error ( "Configuration file '" + filename + "' does not exist." )

#-------------------------------------------------------------------------------

def homeDir():
  return os.environ["HOME"]

#-------------------------------------------------------------------------------

def morselSystem():
  try:
    return os.environ["MORSEL_HOME"]
  except KeyError:
    return MORSEL_FILE_PATH

#-------------------------------------------------------------------------------

def morselUser():
  return homeDir() + "/.morsel"

#-------------------------------------------------------------------------------

def findFile( filename ):
  '''Finds a filename in all search paths according to its extension.'''
  if os.path.exists( filename ):
    return os.path.abspath( filename )

  name, extension = os.path.splitext( filename )
  extension = extension[1:]
  if paths.has_key( extension ):
    for path in paths[extension]:
      resultPath = os.path.join( path, filename )
      if os.path.exists( resultPath ):
        return os.path.abspath( resultPath )
  print "Warning: file %s not found" % filename
  return None

#-------------------------------------------------------------------------------
# Configuration Functions
#-------------------------------------------------------------------------------

def addPath( extension, path  ):
  '''Adds a search path for the given extension.'''
  if not paths.has_key( extension ):
    paths[extension] = []
  if not path in paths[extension]:
    paths[extension].append( path )

#-------------------------------------------------------------------------------

def addMorselPath( extension, path ):
  addPath( extension, os.path.join( ".", path ) )
  addPath( extension, os.path.join( morselUser(), path ) )
  addPath( extension, os.path.join( morselSystem(), path ) )

#-------------------------------------------------------------------------------

def fullscreen( value ):
  '''Selects fullscreen or windowed mode.'''
  if value:
    panda.loadPrcFileData("", "fullscreen 1")
  else:
    panda.loadPrcFileData("", "fullscreen 0")

#-------------------------------------------------------------------------------

def windowSize( width, height ):
  '''Sets the window width and height for windowed mode.'''
  panda.loadPrcFileData("", "win-size %s %s" % ( width, height ) )

#-------------------------------------------------------------------------------
# Module Variables
#-------------------------------------------------------------------------------

paths = {}
meshes = {}
actors = {}


