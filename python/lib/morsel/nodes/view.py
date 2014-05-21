from node import Node

#-------------------------------------------------------------------------------

class View(Node):
  def __init__(self, world = None, **kargs):
    self.world = world
    
    super(View, self).__init__(**kargs)

    if self.world:
      self.world.addView(self)
    
#-------------------------------------------------------------------------------

  def draw(self):
    pass
