from morsel.core import *
from morsel.nodes.controller import Controller

import pygame.joystick

#-------------------------------------------------------------------------------

class Joystick(Controller):
  def __init__(self, world, name = "Joystick", device = 0, axes = [0, 1],
      **kargs):
    Controller.__init__(self, world, name = name, **kargs)

    self.device = device
    self.axes = axes
    
    pygame.init()
    pygame.joystick.init()
    self.joystick = pygame.joystick.Joystick(device)
    self.joystick.init()
    
#-------------------------------------------------------------------------------

  def __del__(self):
    pygame.joystick.quit()

#-------------------------------------------------------------------------------
  
  def updateCommand(self, period):
    pygame.event.pump()

    command = [0]*len(self.actuator.command)
    state = self.actuator.state
    
    for i in range(len(command)):
      command[i] = (-self.joystick.get_axis(self.axes[i])*
        self.actuator.limits[i][1])
      acceleration = (command[i]-state[i])/period
      maxAcceleration = (self.actuator.limits[i][1]-
        self.actuator.limits[i][0])/period
      maxDeceleration = maxAcceleration
    
      if state[i] == 0:
        if acceleration > maxAcceleration:
          command[i] = maxAcceleration*period
        elif acceleration < -maxAcceleration:
          command[i] = -maxAcceleration*period
      elif state[i] > 0:
        if acceleration > maxAcceleration:
          command[i] = state[i]+maxAcceleration*period
        elif acceleration < -maxDeceleration:
          command[i] = state[i]-maxDeceleration*period
      elif state[i] < 0:
        if acceleration < -maxAcceleration:
          command[i] = state[i]-maxAcceleration*period
        elif acceleration > maxDeceleration:
          command[i] = state[i]+maxDeceleration*period

    self.actuator.command = command
