from node import Node

#-------------------------------------------------------------------------------

class Actor(Node):
  def __init__(self, world, name, **kargs):
    Node.__init__(self, world, name, **kargs)

#-------------------------------------------------------------------------------

  def updatePhysics(self, period):
    pass

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    pass
