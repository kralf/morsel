from morsel.core import *
from controller import Controller

import pygame.joystick

#-------------------------------------------------------------------------------

class Joystick(Controller):
  def __init__(self, name = "Joystick", platform = None, device = 0,
      axes = [0, 1]):
    Controller.__init__(self, name = name, platform = platform)

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

    command = [0]*len(self.platform.command)
    state = self.platform.state
    
    for i in range(len(command)):
      command[i] = (-self.joystick.get_axis(self.axes[i])*
        self.platform.limits[i][1])
      acceleration = (command[i]-state[i])/period
      maxAcceleration = (self.platform.limits[i][1]-
        self.platform.limits[i][0])/period
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

    self.platform.command = command
