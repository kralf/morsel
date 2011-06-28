import morsel.input

#-------------------------------------------------------------------------------

def KeyboardController( object, *args, **kargs ):
  result = input.KeyboardController( object, *args, **kargs )
  return result
  
#-------------------------------------------------------------------------------

def JoystickController( object, *args, **kargs ):
  result = input.JoystickController( object, *args, **kargs )
  return result
  
#-------------------------------------------------------------------------------

def RandomController( object ):
  result = input.RandomController( speed = 10, steeringRate = 45 )
  result.add( object )
  return result
  

