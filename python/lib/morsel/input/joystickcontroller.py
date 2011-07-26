from   morsel.core import *
import pygame.joystick


class JoystickController( object ):

  #-----------------------------------------------------------------------------
  
  def __init__( self, platform ):
    self.platform = platform
    scheduler.addTask( "stepJoystickController", self.step )
    pygame.init()
    pygame.joystick.init()
    self.joystick = pygame.joystick.Joystick( 0 )
    self.joystick.init()
    self.oldTime  = None
    self.velocity = 0
    
  #-----------------------------------------------------------------------------
  
  def step( self, time ):
    if self.oldTime != None:
      pygame.event.pump()
      command = [0, 0]
      command[0] = -self.joystick.get_axis( 1 ) * self.platform.commandLimits[0][1]
      command[1] = -self.joystick.get_axis( 0 ) * self.platform.commandLimits[1][1]

      deltaT  = time - self.oldTime
      deltaV  = command[0] - self.velocity
      acceleration    = deltaV / deltaT
      maxAcceleration = self.platform.commandLimits[0][1] / 2
      maxDeceleration = self.platform.commandLimits[0][1]
      if self.velocity == 0:
        if acceleration > maxAcceleration:
          command[0] = maxAcceleration * deltaT
        elif acceleration < -maxAcceleration:
          command[0] = -maxAcceleration * deltaT
      elif self.velocity > 0:
        if acceleration > maxAcceleration:
          command[0] = self.velocity + maxAcceleration * deltaT
        elif acceleration < -maxDeceleration:
          command[0] = self.velocity - maxDeceleration * deltaT
      elif self.velocity < 0:
        if acceleration < -maxAcceleration:
          command[0] = self.velocity - maxAcceleration * deltaT
        elif acceleration > maxDeceleration:
          command[0] = self.velocity + maxDeceleration * deltaT
          
      self.velocity         = command[0]
      self.platform.setCommand(command)
          
    self.oldTime = time
    return True
