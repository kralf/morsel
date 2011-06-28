from morsel.core import *
from math import *

#-------------------------------------------------------------------------------

def bounds( mesh ):
  hpr = mesh.getHpr()
  mesh.setHpr( 0, 0, 0 )
  bounds = mesh.getTightBounds()
  lx = bounds[1][0] - bounds[0][0]
  ly = bounds[1][1] - bounds[0][1]
  lz = bounds[1][2] - bounds[0][2]
  mesh.setHpr( hpr )
  return lx, ly, lz
  
#-------------------------------------------------------------------------------

def updateFromBody( node, body ):
  panda.NodePath.setPos( node, body.getPosition() )
  q = body.getQuaternion()
  node.setQuat( panda.Quat( q[0], q[1], q[2], q[3] ) )

#-------------------------------------------------------------------------------

def updatePosFromBody( node, body ):
  panda.NodePath.setPos( node, body.getPosition() )
  
#-------------------------------------------------------------------------------

def updateHprFromBody( node, body ):
  q = body.getQuaternion()
  panda.NodePath.setQuat( node, panda.Quat( q[0], q[1], q[2], q[3] ) )

#-------------------------------------------------------------------------------

def erp( mass, period, damping, delta ):
  frequency = 2 * pi / period
  return delta * frequency / ( delta * frequency + 2 * damping )

#-------------------------------------------------------------------------------

def cfm( mass, period, damping, delta ):
  frequency = 2 * pi / period
  return erp( mass, period, damping, delta ) / ( delta * frequency ** 2 * mass )
