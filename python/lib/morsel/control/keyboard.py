from morsel.core import *
from morsel.nodes.controller import Controller

#-------------------------------------------------------------------------------

class Keyboard(Controller):
  def __init__(self, world, name = "Keyboard",
      keys = [("arrow_down","arrow_up"), ("arrow_right", "arrow_left")],
      delay = [1, 1], **kargs):
    Controller.__init__(self, world, name = name, **kargs)

    self.delay = delay
    self.keys = keys
    
#-------------------------------------------------------------------------------

  def setKey(self, key, value):
    self.keyMap[key] = value

  def getKey(self, key):
    return self.keyMap[key]

#-------------------------------------------------------------------------------

  def setKeys(self, keys):
    self._keys = keys

    self.keyMap = {}
    self.increments = []
    
    for i in range(len(self._keys)):
      self.keyMap[self._keys[i][0]] = 0
      base.accept(self._keys[i][0], self.setKey, [self._keys[i][0], 1])
      base.accept(self._keys[i][0]+"-up", self.setKey, [self._keys[i][0], 0])

      self.keyMap[self._keys[i][1]] = 0
      base.accept(self._keys[i][1], self.setKey, [self._keys[i][1], 1])
      base.accept(self._keys[i][1]+"-up", self.setKey, [self._keys[i][1], 0])

      self.increments.append(      
        (self.platform.limits[i][1]-self.platform.limits[i][0])/self.delay[i])

  def getKeys(self):
    return self._keys

  keys = property(getKeys, setKeys)

#-------------------------------------------------------------------------------

  def updateCommand(self, period):
    command = self.platform.command

    for i in range(len(command)):
      if self.keyMap[self.keys[i][0]]:
        command[i] -= self.increments[i]*period
        command[i] = max(command[i], self.platform.limits[i][0])
      elif self.keyMap[self.keys[i][1]]:
        command[i] += self.increments[i]*period
        command[i] = min(command[i], self.platform.limits[i][1])
      elif command[i] != 0:
          command[i] -= self.increments[i]*period*command[i]/abs(command[i])
          if abs(command[i]) <= abs(self.increments[i]*period):
            command[i] = 0

    self.platform.command = command
