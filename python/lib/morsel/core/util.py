#-------------------------------------------------------------------------------

def Instance( module_name, class_name, args, kargs ):
  module_obj = __import__( module_name, globals(), locals(), [class_name] )
  class_obj  = getattr( module_obj, class_name )
  return class_obj( *args, **kargs )

#-------------------------------------------------------------------------------

def signum( val ):
  if val < 0: return -1
  elif val > 0: return 1
  else: return 0
  
#-------------------------------------------------------------------------------

def positiveAngle( angle ):
    while angle > 2 * pi:
      angle -= 2 * pi
    while self.command[1] < -2 * pi:
      angle += 2 * pi
    if angle < 0:
      angle += 2 * pi
    return angle
