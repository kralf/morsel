from morsel.panda import *
from morsel.nodes.controller import Controller
from morsel.core.event_handler import EventHandler

#-------------------------------------------------------------------------------

class Keyboard(Controller):
  def __init__(self, name = "Keyboard", keys = [("arrow_down","arrow_up"),
      ("arrow_right", "arrow_left")], delay = None, **kargs):
    Controller.__init__(self, name = name, **kargs)

    self.delay = delay
    if not self.delay:
      self.delay = [1]*len(keys)
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
      if self._keys[i]:
        self.keyMap[self._keys[i][0]] = False
        framework.eventManager.addHandler(self._keys[i][0],
          EventHandler(self.setKey, self._keys[i][0], True))
        framework.eventManager.addHandler(self._keys[i][0]+"-up",
          EventHandler(self.setKey, self._keys[i][0], False))

        self.keyMap[self._keys[i][1]] = False
        framework.eventManager.addHandler(self._keys[i][1],
          EventHandler(self.setKey, self._keys[i][1], True))
        framework.eventManager.addHandler(self._keys[i][1]+"-up",
          EventHandler(self.setKey, self._keys[i][1], False))

      self.increments.append(
        (self.actuator.limits[i][1]-self.actuator.limits[i][0])/self.delay[i])

  def getKeys(self):
    return self._keys

  keys = property(getKeys, setKeys)

#-------------------------------------------------------------------------------

  def updateCommand(self, period):
    command = self.actuator.command

    for i in range(min(len(self.keys), len(command))):
      if self.keys[i]:
        if self.keyMap[self.keys[i][0]]:
          command[i] -= self.increments[i]*period
          command[i] = max(command[i], self.actuator.limits[i][0])
        elif self.keyMap[self.keys[i][1]]:
          command[i] += self.increments[i]*period
          command[i] = min(command[i], self.actuator.limits[i][1])
        elif command[i] != 0:
          command[i] -= self.increments[i]*period*command[i]/abs(command[i])
          if abs(command[i]) <= abs(self.increments[i]*period):
            command[i] = 0

    self.actuator.command = command
