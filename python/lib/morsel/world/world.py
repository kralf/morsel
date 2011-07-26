from morsel.nodes import *

#-------------------------------------------------------------------------------

class World:
  def __init__(self, physics):
    object.__init__(self)
    
    self.physics = physics
    self.scene = Scene(self)
    
    scheduler.addTask("WorldUpdater", self.update)
    
#-------------------------------------------------------------------------------
  
  def update(self, time):
    return True
