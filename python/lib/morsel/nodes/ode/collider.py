from morsel.core import *
from morsel.nodes.collection import Collection
from morsel.nodes.iterator import Iterator
from morsel.nodes.solid import Solid

#-------------------------------------------------------------------------------

class Collider(Collection):
  def __init__(self, world, name, **kargs):
    Collection.__init__(self, world, name, **kargs)
    
    self.hide()

#-------------------------------------------------------------------------------

  def getSolids(self):
    return Iterator(self, Solid).generator

  solids = property(getSolids)

#-------------------------------------------------------------------------------

  def setCollisionMasks(self, collisionsFrom, collisionsInto):
    for solid in self.solids:
      if solid.geometry:
        solid.setCollisionMasks(collisionsFrom, collisionsInto)
