from object import Object

#-------------------------------------------------------------------------------

class Sensor(Object):
  def __init__(self, **kargs):
    super(Sensor, self).__init__(**kargs)
    
    if self.world:
      self.world.addSensor(self)
      
#-------------------------------------------------------------------------------

  def step(self, period):
    pass
  