from morsel.world.globals import *
from node import Node

#-------------------------------------------------------------------------------

class View(Node):
  def __init__(self, world, name, **kargs):
    Node.__init__(self, world, name, **kargs)

#-------------------------------------------------------------------------------

  def update(self):
    pass
