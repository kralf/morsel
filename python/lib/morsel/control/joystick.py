from morsel.panda import *
from morsel.nodes.controller import Controller

import pygame.joystick

#-------------------------------------------------------------------------------

class Joystick(Controller):
  def __init__(self, device = None, axes = [], scales = [], **kargs):
    super(Joystick, self).__init__(**kargs)

    self.device = device
    self.axes = axes
    self.scales = scales
    self.joystick = None

    if self.device is not None:
      pygame.init()
      pygame.joystick.init()
      self.joystick = pygame.joystick.Joystick(self.device)
      self.joystick.init()
    
#-------------------------------------------------------------------------------

  def __del__(self):
    if self.joystick:
      pygame.joystick.quit()

#-------------------------------------------------------------------------------

  def setAxis(self, axis, value):
    self.axisMap[axis] = value

  def getAxis(self, axis):
    return self.axisMap[axis]

#-------------------------------------------------------------------------------

  def setAxes(self, axes):
    self._axes = axes
    
    self.axisMap = {}

    for i in range(len(self._axes)):
      self.axisMap[self._axes[i]] = 0

  def getAxes(self):
    return self._axes

  axes = property(getAxes, setAxes)

#-------------------------------------------------------------------------------
  
  def step(self, period):
    command = [0]*len(self.actuator.command)
    state = self.actuator.state

    if self.joystick:
      pygame.event.pump()
      for i in range(len(self.axes)):
        self.setAxis(self.axes[i], self.joystick.get_axis(self.axes[i]))

    for i in range(min(len(self.axes), len(command))):
      if self.scales and (i < len(self.scales)):
        scale = self.scales[i]
      else:
        scale = 1
      
      command[i] = scale*self.axisMap[self.axes[i]]*self.actuator.limits[i][1]
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
