import morsel.input

#-------------------------------------------------------------------------------

def KeyboardController( object, *args, **kargs ):
  result = morsel.input.KeyboardController( object, *args, **kargs )
  return result
  
#-------------------------------------------------------------------------------

def JoystickController( object, *args, **kargs ):
  result = morsel.input.JoystickController( object, *args, **kargs )
  return result
  
#-------------------------------------------------------------------------------

def RandomController( object ):
  result = morsel.input.RandomController( speed = 10, steeringRate = 45 )
  result.add( object )
  return result
  

