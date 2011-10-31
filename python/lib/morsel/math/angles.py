from math import *

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
