from morsel.core import *
from tube import Tube

#-------------------------------------------------------------------------------

class Cylinder(Tube):
  def __init__(self, world, name, mesh, **kargs):
    Tube.__init__(self, world, name, mesh, **kargs)
