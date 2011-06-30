from morsel.core import *
from math import *

EPSILON = 1E-6

class Ackermann( panda.NodePath ):
  def __init__( self, name, maxSpeed, maxAcceleration,
                maxDeceleration, maxSteeringAngle, maxSteeringRate,
                axesDistance, mesh, **kargs ):
    object.__init__( self )
    panda.NodePath.__init__( self, name )
    self.reparentTo( render )
    self.__mesh  = loadMesh( name + "Mesh", mesh )
    self.__mesh.reparentTo( self )    
    self._pose = [0, 0, 0]
    self._command = [0, 0]
    self.real = [0, 0]
    self.maxSpeed = maxSpeed
    self.maxAcceleration = maxAcceleration
    self.maxDeceleration = maxDeceleration
    self._maxSteeringAngle = maxSteeringAngle * pi / 180
    self._maxSteeringRate = maxSteeringRate * pi / 180
    self.axesDistance = axesDistance
    self._position = [0] * 3
    self._orientation = [0] * 3
    self.commandSize = 2
    self.commandLimits = [
      ( -maxSpeed, maxSpeed),
      ( -maxSteeringAngle, maxSteeringAngle )
    ]

  def updatePhysics( self, dt ):
    # Update Longitudinal speed
    dv = self.command[0] - self.real[0]
    if dv > -self.maxDeceleration * dt and dv < self.maxAcceleration * dt:
      self.real[0] = self.command[0]
    else:
      if dv < 0:
        self.real[0] -= self.maxDeceleration * dt
      else:
        self.real[0] += self.maxAcceleration * dt
    if self.real[0] > self.maxSpeed:
      self.real[0] = self.maxSpeed
    elif self.real[0] < 0:
      self.real[0] = 0
    
    # Update Steering angle
    if abs( self.real[1] - self.command[1] ) < self._maxSteeringRate * dt:
      self.real[1] = self.command[1]
    else:
      self.real[1] += signum( self.command[1] - self.real[1] ) * self._maxSteeringRate * dt
    if self.real[1] > self._maxSteeringAngle:
      self.real[1] = self._maxSteeringAngle
    elif self.real[1] < - self._maxSteeringAngle:
      self.real[1] = -self._maxSteeringAngle
    
    # Update State
    if abs( self.real[1] ) < EPSILON:
      dx = self.real[0] * dt
      dy = 0
      dtheta = 0
    else:
      r = self.axesDistance / tan( self.real[1] )
      dtheta = self.real[0] * dt / r
      dx = r * sin( dtheta )
      dy = r * ( 1 - cos( dtheta ) )
    self._pose[0] += dx * cos( self._pose[2] ) - dy * sin( self._pose[2] )
    self._pose[1] += dx * sin( self._pose[2] ) + dy * cos( self._pose[2] )
    self._pose[2] += dtheta

  def updateGraphics( self ):
    NodePath.setX( self, self._pose[0] )
    NodePath.setY( self, self._pose[1] )
    NodePath.setH( self, self._pose[2] * 180 / pi )

  def getCommand( self ):
    return self._command
    
  def setCommand( self, *args ):
    assert 0 < len( args ) <= 2
    
    if len( args ) == 1:
      self._command = args[0]
    elif len( args ) == 2:
      self._command = [ args[0], args[1] * pi / 180 ]
      
    return self._command
    
  command = property( getCommand, setCommand )

  def setPos( self, position ):
    NodePath.setPos( self, position )
    self._pose[0] = position[0]
    self._pose[1] = position[1]

    
  def setHpr( self, hpr ):
    NodePath.setHpr( self, hpr )
    self._pose[2] = hpr[0] * pi / 180
