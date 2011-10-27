from node import Node
from iterator import Iterator
from facade import Collider

#-------------------------------------------------------------------------------

class Solid(Node):
  def __init__(self, world, name, mesh = None, parent = None, **kargs):
    if not isinstance(parent, Solid):
      if not parent.collider:
        parent.collider = Collider(parent.name+"Collider", parent = parent)
      Node.__init__(self, world, name, parent = parent.collider, **kargs)
    else:
      Node.__init__(self, world, name, parent = parent, **kargs)

    parent.collider.addSolid(self)
    
    self.mesh = mesh

#-------------------------------------------------------------------------------

  def setPosition(self, position, node = None, recursive = True):
    Node.setPosition(self, position, node)

    if recursive:
      for child in self.getChildren(Solid):
        child.position = child.position

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None, recursive = True):
    Node.setOrientation(self, orientation, node)

    if recursive:
      for child in self.getChildren(Solid):
        child.orientation = child.orientation

  orientation = property(Node.getOrientation, setOrientation)
