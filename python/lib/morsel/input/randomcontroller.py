from morsel.core.framework import *
from random import *

class RandomController( object ):
  
  def __init__( self, name, speed, steeringRate ):
    self.speed = speed
    self.steeringRate = steeringRate
    self.platforms = []
    scheduler.addTask( name + "RandomController", self.step )
    
  def step( self, time ):
    forward = 1
    left = 0
    right = 0
    if randint( 0, 10) > 5:
      if randint( 0, 10 ) > 3:
        left = 1
      else:
        right = 1
      
    v = [0, 0]
    if forward != 0:
      v[0] = self.speed
    else:
      v[0] = 0
      
    if left != 0:
      v[1] = self.steeringRate
    elif right != 0:
      v[1] = -self.steeringRate
      
    for platform in self.platforms:
      platform.setCommand(v)
    return True
    
  def add( self, platform ):
    self.platforms.append( platform )
