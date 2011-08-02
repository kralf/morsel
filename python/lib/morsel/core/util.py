from math import *

#-------------------------------------------------------------------------------

def signum(val):
  if val < 0:
    return -1
  elif val > 0:
    return 1
  else:
    return 0
  
#-------------------------------------------------------------------------------

def correctAngle(angle):
    while angle > 180:
      angle -= 360
    while angle < -180:
      angle += 360
    return angle

#-------------------------------------------------------------------------------

def positiveAngle(angle):
    angle = correctAngle(angle)
    if angle < 0:
      angle += 360
    return angle

#-------------------------------------------------------------------------------

def flatten(*args):
  for arg in args:
    if type(arg) in (type(()),type([])):
      for element in arg:
        for f in flatten(element):
          yield f
    else:
      yield arg
