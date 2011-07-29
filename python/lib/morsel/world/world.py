from morsel.nodes.scene import Scene

#-------------------------------------------------------------------------------

class World:
  def __init__(self, physics):
    object.__init__(self)
    
    self.physics = physics
    self.scene = None
    
    scheduler.addTask("WorldUpdate", self.update)
    
#-------------------------------------------------------------------------------
  
  def update(self, time):
    return True
