from morsel.panda import *
from morsel.nodes.panda.solids import Tube

#-------------------------------------------------------------------------------

class Cylinder(Tube):
  def __init__(self, **kargs):
    super(Cylinder, self).__init__(**kargs)
