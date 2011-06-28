from morsel.core import *

#-------------------------------------------------------------------------------

class KeyboardController( object ):
  
  def __init__( self, platform, axis1Time = 1, axis2Time = 1 ):
    self.platform = platform
    self.keyMap = {"left":0, "right":0, "forward":0, "back":0 }
    base.accept("arrow_left", self.setKey, ["left",1])
    base.accept("arrow_right", self.setKey, ["right",1])
    base.accept("arrow_up", self.setKey, ["forward",1])
    base.accept("arrow_down", self.setKey, ["back",1])
    base.accept("arrow_left-up", self.setKey, ["left",0])
    base.accept("arrow_right-up", self.setKey, ["right",0])
    base.accept("arrow_up-up", self.setKey, ["forward",0])
    base.accept("arrow_down-up", self.setKey, ["back",0])
    scheduler.addTask( "stepKeyboardController", self.step )
    self.increments = [
      platform.commandLimits[0][1] - platform.commandLimits[0][0] / axis1Time,
      platform.commandLimits[1][1] - platform.commandLimits[1][0] / axis2Time
    ]
    self.lastTime = 0
    
  def setKey( self, key, value ):
    self.keyMap[key] = value

  def step( self, time ):
    v = [x for x in self.platform.command]
    a = 0
    delta = time - self.lastTime
    if self.keyMap["forward"] != 0:
      v[a] += self.increments[a] * delta
      v[a] = min( v[a], self.platform.commandLimits[a][1] )
    elif self.keyMap["back"] !=0:
      v[a] -= self.increments[a] * delta
      v[a] = max( v[a], self.platform.commandLimits[0][0] )
    else:
      if v[a] != 0:
        v[a] = v[a] - self.increments[a]  * delta  * v[a] / abs( v[a] )
        if abs( v[a] ) <= abs( self.increments[a] * delta ):
          v[a] = 0

    a = 1
    if self.keyMap["left"] != 0:
      v[a] += self.increments[a] * delta
      v[a] = min( v[a], self.platform.commandLimits[a][1] )
    elif self.keyMap["right"] != 0:
      v[a] -= self.increments[a] * delta
      v[a] = max( v[a], self.platform.commandLimits[a][0] )
    else:
      if v[a] != 0:
        v[a] = v[a] - self.increments[a] * delta * v[a] / abs( v[a] )
        if abs( v[a] ) <= abs( self.increments[a] * delta ):
          v[a] = 0
    self.platform.command = v
    self.lastTime = time
    return True
