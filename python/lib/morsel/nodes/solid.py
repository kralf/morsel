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

  def setPosition(self, position, node = None):
    Node.setPosition(self, position, node)
    self.updateTransform()

  position = property(Node.getPosition, setPosition)

#-------------------------------------------------------------------------------

  def setOrientation(self, orientation, node = None):
    Node.setOrientation(self, orientation, node)
    self.updateTransform()

  orientation = property(Node.getOrientation, setOrientation)

#-------------------------------------------------------------------------------

  def updateTransform(self):
    pass
  